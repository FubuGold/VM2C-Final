import gurobipy as gp  # import the installed package
from gurobipy import GRB

# --------------------------------
# Create constant
N_CHAIN, N_SHIFT, N_SKILL = 3,3,3

# --------------------------------
# Create model
params = {
"WLSACCESSID": 'f164f691-1d84-4092-a810-e324efa273f0',
"WLSSECRET": '52be21e1-ad4a-439a-9963-1d8af268ab0e',
"LICENSEID": 2395694,
}
env = gp.Env(params=params)

# --------------------------------
# Read input
skill = []
timetable = []
chain_need = []
id_to_code = {}
# Rot - May_dong_hop - Pallet
with open("FormattedInput.txt","r") as f:
    n_worker = int(f.readline().split()[0])
    for _ in range(3):
        tmp = []
        for i in range(n_worker):
            tmp.append(list(map(int,f.readline().split())))
        skill.append(tmp)
        f.readline()

    for id in range(3):
        chain_need.append(list(map(int,f.readline().split())))
    f.readline()

    for i in range(29):
        tmp1 = []
        for j in range(3):
            tmp1.append(list(map(int,f.readline().split())))
        timetable.append(tmp1)
        f.readline()
    
    for i in range(n_worker):
        k,v = map(str,f.readline().split())
        id_to_code[int(k)] = v


skill = np.array(skill) # Chain - Worker - Skill
timetable = np.array(timetable) # Day - Chain - Shift
chain_need = np.array(chain_need) # Chain - Skill
# print(skill)
print(timetable)
# print(chain_need)

# --------------------------------
def ScheduleDay(prevSchedule,day):
    model = gp.Model(env=env) # Create Model

    # Create Variable
    lmao = model.addMVar(shape = (3,3,n_worker,3), vtype = GRB.BINARY)
    #                Chain - Shift - Worker - Skill

    # Create Constraint
    
    for chain in range(N_CHAIN):
        for sk in range(N_SKILL):
            for shift in range(N_SHIFT):
                model.addConstr(lmao[chain,shift,:,sk].sum() == chain_need[chain,sk])
        for ppl in range(n_worker):
            for sk in range(N_SKILL):
                model.addConstr(lmao[chain,:,ppl,sk].sum() <= skill[chain,ppl,sk])

    model.addConstrs(lmao[:,:,ppl,:].sum() <= 1 for ppl in range(n_worker))
    model.addConstrs(lmao[:,0,ppl,:].sum() <= 1 - prevSchedule[:,2,ppl,:].sum() for ppl in range(n_worker))
    
    model.setObjective(lmao.sum(),sense = GRB.MINIMIZE)

    model.optimize()

    if model.status == GRB.OPTIMAL:
        return lmao.x[0].astype(int)
    else: return -1
    
def main():
    prevSchedule = np.zeros((3,3,17,3))
    day = 1
    res = ScheduleDay(prevSchedule=prevSchedule,day=day)
    for chain in range(N_CHAIN):
        for shift in range(N_SHIFT):
            for sk in range(N_SKILL):
                for ppl in range(n_worker):
                    if res[chain,shift,ppl,sk]: 
                        ...
                        

if __name__ == "__main__":
    # main()
    ...