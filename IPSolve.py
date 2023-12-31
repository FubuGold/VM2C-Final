import FormatInput
import numpy as np
import gurobipy as gp  # import the installed package
from gurobipy import GRB
import matplotlib.pyplot as plt 
# --------------------------------
# Create constant, variable
N_CHAIN, N_SHIFT, N_SKILL = 3,3,3

datapack = 1

skill = []
timetable = []
chain_need = []

id_to_code = {}
id_to_skill = {0 : "Rot", 1 : "May_dong_hop", 2 : "Pallet"}

shift_count = None

# --------------------------------
# Create Input
def createInput():
    global datapack
    reader = FormatInput.Readfile()
    reader.printInputIP(datapack=datapack)
createInput() # Comment nếu đã tạo. Chạy nếu thay đổi dataset

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
shift_count = np.zeros((n_worker,2)) # Worker - Shift (Total - Night)
chosen = np.zeros((n_worker))

# print(skill)
# print(timetable)
# print(chain_need)

# --------------------------------
# Model
def ScheduleDay(nightWorker,day,prob,stage = 1):

    model = gp.Model(env=env) # Create Model
    model.params.NonConvex = 2

    # Create Variable
    lmao = model.addMVar(shape = (N_CHAIN,N_SHIFT,n_worker,N_SKILL), vtype = GRB.BINARY)
    #                               Chain - Shift - Worker - Skill

    # Create Constraint
    for chain in range(N_CHAIN):
        for sk in range(N_SKILL):
            for shift in range(N_SHIFT):
                model.addConstr(lmao[chain,shift,:,sk].sum() == chain_need[chain,sk]*timetable[day,chain,shift]) # Đủ nhân lực cho từng công việc từng dây chuyền từng ca 
        for ppl in range(n_worker):
            for sk in range(N_SKILL):
                model.addConstr(lmao[chain,:,ppl,sk].sum() <= skill[chain,ppl,sk]) # Nhân sự làm đúng kĩ năng

    model.addConstrs(lmao[:,:,ppl,:].sum() <= 1 for ppl in range(n_worker)) # Mỗi ngày làm 1 việc 1 ca 1 dây chuyền
    model.addConstrs(lmao[:,0,ppl,:].sum() <= 0 for ppl in nightWorker) # Làm ca 3 hôm trước ko làm ca 1 hôm sau

    if (prob == 2):
        model.addConstrs(lmao[:,:,ppl,:].sum() + shift_count[ppl,0] <= 24 for ppl in range(n_worker))
    
    if (prob == 2 and stage == 2):
        model.addConstrs(lmao[:,:,ppl,:].sum() <= chosen[ppl] for ppl in range(n_worker))
        

    # Set objective
    if (prob == 1) or (prob == 2 and stage == 2):
        max_shift = model.addVar(vtype = GRB.INTEGER)
        min_shift = model.addVar(vtype = GRB.INTEGER)

        max_shift_night = model.addVar(vtype = GRB.INTEGER)
        min_shift_night = model.addVar(vtype = GRB.INTEGER)
        
        if prob == 2:
            for ppl in range(n_worker):
                if chosen[ppl]:
                    model.addConstr(lmao[:,:,ppl,:].sum() + shift_count[ppl,0] <= max_shift)
                    model.addConstr(lmao[:,:,ppl,:].sum() + shift_count[ppl,0] >= min_shift)

                    model.addConstr(lmao[:,2,ppl,:].sum() + shift_count[ppl,1] <= max_shift_night)
                    model.addConstr(lmao[:,2,ppl,:].sum() + shift_count[ppl,1] >= min_shift_night)
        else:
            model.addConstrs(lmao[:,:,ppl,:].sum() + shift_count[ppl,0] <= max_shift for ppl in range(n_worker))
            model.addConstrs(lmao[:,:,ppl,:].sum() + shift_count[ppl,0] >= min_shift for ppl in range(n_worker))

            model.addConstrs(lmao[:,2,ppl,:].sum() + shift_count[ppl,1] <= max_shift_night for ppl in range(n_worker))
            model.addConstrs(lmao[:,2,ppl,:].sum() + shift_count[ppl,1] >= min_shift_night for ppl in range(n_worker))
        
        # obj = (max_shift - min_shift) * (max_shift_night - min_shift_night)
        obj =  (max_shift - min_shift) * (max_shift - min_shift) + (max_shift_night - min_shift_night) * (max_shift_night - min_shift_night)
        
        model.setObjective(obj,sense = GRB.MINIMIZE)
    else:
        obj = sum([(chosen[ppl] + lmao[:,:,ppl,:].sum())*(chosen[ppl] + lmao[:,:,ppl,:].sum()) for ppl in range(n_worker)])
        model.setObjective(obj,sense = GRB.MAXIMIZE)

    model.optimize()

    tmp = model.status

    if tmp == GRB.OPTIMAL:
        return lmao.x.astype(int),obj.getValue()
    else: return -1
    
    
def solve_a():
    global datapack
    global shift_count
    shift_count = np.zeros((n_worker,2))
    if datapack == 1: f = open("result_data_1_part_a.txt","w")
    else: f = open("result_data_2_part_a.txt","w")
    result = []
    nightWorker = []
    for day in range(1,29):
        res = ScheduleDay(nightWorker=nightWorker,day=day,prob=1)
        nightWorker = []
        if res == -1:
            print("Falled\n")
            break
        res,obj = res
        for chain in range(N_CHAIN):
            for shift in range(N_SHIFT):
                for sk in range(N_SKILL):
                    for ppl in range(n_worker):
                        if res[chain,shift,ppl,sk]:
                            tmp = str(day)
                            if len(tmp) == 1: tmp = "0" + tmp
                            f.write(f"{tmp}.06.2023 Ca_{shift+1} {id_to_code[ppl]} Day_chuyen_{chain+1} {id_to_skill[sk]}\n")
        for ppl in range(n_worker):
            if res[:,2,ppl,:].sum() == 1:
                nightWorker.append(ppl)
        
        result.append(obj)         
        for ppl in range(n_worker):
            shift_count[ppl,0] += res[:,:,ppl,:].sum()
            shift_count[ppl,1] += res[:,2,ppl,:].sum()
    print(np.array(result).shape)
    print(shift_count)
    print(n_worker)
    plt.plot(np.array(result))
    plt.show()
    f.close()

def solve_b():
    global chosen
    global datapack
    global shift_count
    nightWorker = []
    if datapack == 1: f = open("result_data_1_part_b.txt","w")
    else: f = open("result_data_2_part_b.txt","w")
    result = []
    for day in range(1,29):
        res = ScheduleDay(nightWorker=nightWorker,day=day,prob=2,stage=1)
        nightWorker = []
        if res == -1:
            print(f"Falled {day}\n")
            break
        res,obj = res
        for ppl in range(n_worker):
            if res[:,2,ppl,:].sum() == 1:
                nightWorker.append(ppl)
        
        for ppl in range(n_worker):
            if res[:,:,ppl,:].sum() == 1:
                chosen[ppl] = 1
            shift_count[ppl,0] += res[:,:,ppl,:].sum()
            shift_count[ppl,1] += res[:,2,ppl,:].sum()

    shift_count = np.zeros((n_worker,2))
    nightWorker = []
    for day in range(1,29):
        res = ScheduleDay(nightWorker=nightWorker,day=day,prob=2,stage=2)
        nightWorker = []
        if res == -1:
            print(f"Falled {day}\n")
            break
        res,obj = res
        # print(obj)
        for chain in range(N_CHAIN):
            for shift in range(N_SHIFT):
                for sk in range(N_SKILL):
                    for ppl in range(n_worker):
                        if res[chain,shift,ppl,sk]:
                            tmp = str(day)
                            if len(tmp) == 1: tmp = "0" + tmp
                            f.write(f"{tmp}.06.2023 Ca_{shift+1} {id_to_code[ppl]} Day_chuyen_{chain+1} {id_to_skill[sk]}\n")
        for ppl in range(n_worker):
            if res[:,2,ppl,:].sum() == 1:
                nightWorker.append(ppl)
        result.append(obj)
        for ppl in range(n_worker):
            if res[:,:,ppl,:].sum() == 1:
                chosen[ppl] = 1
    
        for ppl in range(n_worker):
            shift_count[ppl,0] += res[:,:,ppl,:].sum()
            shift_count[ppl,1] += res[:,2,ppl,:].sum()

    print(np.array(result).shape)
    print(shift_count)
    plt.plot(np.array(result))
    plt.show()

    f.close()
    # print(chosen.nonzero())
    # print(np.array(list(range(55)))[day_left == 24])
        


if __name__ == "__main__":
    # solve_a()
    solve_b()