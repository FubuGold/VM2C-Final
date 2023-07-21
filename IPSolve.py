import numpy as np
import gurobipy as gp  # import the installed package
from gurobipy import GRB
import matplotlib.pyplot as plt 
# --------------------------------
# Create constant, variable
N_CHAIN, N_SHIFT, N_SKILL = 3,3,3
skill = []
timetable = []
chain_need = []

id_to_code = {}
id_to_skill = {0 : "Rot", 1 : "May_dong_hop", 2 : "Pallet"}

shift_count = None

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
shift_count = np.zeros((n_worker,2)) # Worker - Shift (Day - Night)
selected = np.zeros((n_worker),dtype=bool)
# print(skill)
# print(timetable)
# print(chain_need)

# --------------------------------
# Create function
def balance(day,night,worker):
    return day + shift_count[worker,0] + (night + shift_count[worker,1]) * 1.2

# --------------------------------
# Model
def ScheduleDay(prevSchedule,day):
    model = gp.Model(env=env) # Create Model

    # Create Variable
    lmao = model.addMVar(shape = (3,3,n_worker,3), vtype = GRB.BINARY)
    #                Chain - Shift - Worker - Skill

    # Create Constraint
    
    for chain in range(N_CHAIN):
        for sk in range(N_SKILL):
            for shift in range(N_SHIFT):
                model.addConstr(lmao[chain,shift,:,sk].sum() == chain_need[chain,sk]*timetable[day,chain,shift]) # Đủ nhân lực cho từng công việc từng dây chuyền từng ca 
        for ppl in range(n_worker):
            for sk in range(N_SKILL):
                model.addConstr(lmao[chain,:,ppl,sk].sum() <= skill[chain,ppl,sk]) # Nhân sự làm đúng kĩ năng

    model.addConstrs(lmao[:,:,ppl,:].sum() <= 1 for ppl in range(n_worker)) # Mỗi ngày làm 1 việc 1 ca 1 dây chuyền
    model.addConstrs(lmao[:,0,ppl,:].sum() <= 1 - prevSchedule[:,2,ppl,:].sum() for ppl in range(n_worker)) # Làm ca 3 hôm trước ko làm ca 1 hôm sau

    # Set objective
    balance_arr = [balance(lmao[:,:2,ppl,:].sum(),lmao[:,2,ppl,:].sum(),ppl) for ppl in range(n_worker)]
    num_of_pair = int((n_worker / 2) * (n_worker - 1))
    obj = 0
    for id1 in range(n_worker):
        for id2 in range(id1,n_worker):
            obj = obj + (balance_arr[id1] - balance_arr[id2]) * (balance_arr[id1] - balance_arr[id2])
        obj = obj / num_of_pair

    model.setObjective(obj,sense = GRB.MINIMIZE)

    model.optimize()

    if model.status == GRB.OPTIMAL:
        return lmao.x.astype(int),obj.getValue()
    else: return -1
    
def solve_a():
    prevSchedule = np.zeros((3,3,n_worker,3))
    datapack = 1
    if datapack == 1: f = open("result_data_1_part_a.txt","w")
    else: f = open("result_data_2_part_a.txt","w")
    result = []
    for day in range(1,29):
        res,obj = ScheduleDay(prevSchedule=prevSchedule,day=day)
        for chain in range(N_CHAIN):
            for shift in range(N_SHIFT):
                for sk in range(N_SKILL):
                    for ppl in range(n_worker):
                        if res[chain,shift,ppl,sk]: 
                            tmp = str(day)
                            if len(tmp) == 1: tmp = "0" + tmp
                            f.write(f"{tmp}.06.2023 Ca_{shift+1} {id_to_code[ppl]} Day_chuyen_{chain+1} {id_to_skill[sk]}\n")
        result.append(obj)                  
        prevSchedule = res
        for ppl in range(n_worker):
            shift_count[ppl,0] += res[:,:2,ppl,:].sum()
            shift_count[ppl,1] += res[:,2,ppl,:].sum()
    print(np.array(result).shape)
    plt.plot(np.array(result))
    plt.show()

def solve_b():
    ...

if __name__ == "__main__":
    solve_a()