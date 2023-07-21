import FormatInput
import numpy as np
import gurobipy as gp  # import the installed package
from gurobipy import GRB

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
# Rot - May_dong_hop - Pallet
with open("FormattedInput.txt","r") as f:
    n = int(f.readline().split()[0])
    for _ in range(3):
        tmp = []
        for i in range(n):
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
        

skill = np.array(skill)
timetable = np.array(timetable)
chain_need = np.array(chain_need)
# print(skill)
# print(timetable)
print(chain_need)

# --------------------------------
def ScheduleDay(prevSchedule):
    model = gp.Model(env=env) # Create Model

    # Create Variable
    lmao = model.addMVar(shape = (3,3,n,3), vtype = GRB.BINARY)
    #                Chain - Shift - Worker - Skill

    # Create Constraint
    
    for chain in range(3):
        for sk in range(3):
            for shift in range(3):
                model.addConstr(lmao[chain,shift,:,sk].sum() == chain_need[chain,sk])
        for ppl in range(n):
            for sk in range(3):
                model.addConstr(lmao[chain,:,ppl,sk].sum() <= skill[chain,ppl,sk])

    model.addConstrs(lmao[:,:,ppl,:].sum() <= 1 for ppl in range(n))
    model.addConstrs(lmao[:,0,ppl,:].sum() <= 1 - prevSchedule[:,2,ppl,:].sum() for ppl in range(n))
    
    model.setObjective(lmao.sum(),sense = GRB.MINIMIZE)

    model.optimize()

    if model.status == GRB.OPTIMAL:
        return lmao.x.astype(int)
    else: return -1
    
def test():
    prevSchedule = np.zeros((3,3,17,3))
    return ScheduleDay(prevSchedule=prevSchedule)

if __name__ == "__main__":
    schedule = test()
    print(schedule.shape)
    ...  