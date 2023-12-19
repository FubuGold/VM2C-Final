import numpy as np
import pandas as pd
import os

HOURS_PER_SHIFT = 8

class Readfile:

    daychuyen_code_to_id = {'Day_chuyen_1' : 0, 'Day_chuyen_2' : 1,'Day_chuyen_3' : 2}
    skill_to_id = {"Rot" : 0, "May_dong_hop" : 1, "Pallet" : 2}
    
    def __init__(self):
        pass

    def readDatasetIP(self,datapack):
        if datapack == 1:
            num_folds = 1
            data_path = r"duLieu1"
        else:
            num_folds = 3
            data_path = r"duLieu2"
        
        timetable = np.zeros( (29,3,3) ,dtype = int)
                                # Ngay Day-Chuyen Ca
        staff = pd.read_csv(f"VM2C/{data_path}/01_nhan_su.txt", sep=" ")
        staff["so_thu_tu"] = staff["so_thu_tu"].apply(lambda x : x - 1)
        code_to_id = dict(zip(staff["ma_nhan_su"], staff["so_thu_tu"]) )
        id_to_code = dict(zip(staff["so_thu_tu"], staff["ma_nhan_su"]) )
         

        skill = np.zeros(shape = (3,len(code_to_id), 3) , dtype = int)

        # rot = 0, pallet = 1, compressor = 2
        for i in range(num_folds): 
         rot = np.loadtxt(f"VM2C/{data_path}/ky_nang_Day_chuyen_{i+1}_Rot.txt",dtype ="str")
         for nhan_vien in rot:
            id = code_to_id[nhan_vien] 
            skill[i,id,0] = 1   

         compressor = np.loadtxt(f"VM2C/{data_path}/ky_nang_Day_chuyen_{i+1}_May_dong_hop.txt",dtype ="str")
         for nhan_vien in compressor:
            id = code_to_id[nhan_vien]
            skill[i,id,1] = 1
        
         pallet = np.loadtxt(f"VM2C/{data_path}/ky_nang_Day_chuyen_{i+1}_Pallet.txt",dtype ="str")
         for nhan_vien in pallet:
            id = code_to_id[nhan_vien]
            skill[i,id,2] = 1

        def convert_to_start_time(_time):
            return 6 if 6 <= _time < 14 else 14 if 14 <= _time < 22 else 22

        def convert_to_end_time(_time):
            return 14 if 6 < _time <= 14 else 22 if 14 < _time <= 22 else 30
         
        with open(f"VM2C/{data_path}/lenh_san_xuat_Day_chuyen_{i+1}.txt","r") as f:
            f.readline()  # Comment line
            _time = [line.strip().split() for line in f.readlines()]

            shift_start_time = [6, 14, 22]
            
            for j in range(len(_time)):
                start_day = int(_time[j][0][8:10])
                start_hour = int(_time[j][1][0:2])

                end_day = int(_time[j][2][8:10])
                end_hour = int(_time[j][3][0:2])
                
                if (start_hour >= 0 and start_hour < shift_start_time[0]):
                    timetable[start_day - 1][i][2] = 1
                    continue
                    
                new_start_hour = convert_to_start_time(start_hour)
                new_end_hour = convert_to_end_time(end_hour)
                active_shifts = (new_end_hour - new_start_hour) // HOURS_PER_SHIFT
                    
                shifts = [1] * active_shifts
                if (new_start_hour == shift_start_time[0]):
                    timetable[start_day][i][:active_shifts] = shifts
                elif (new_start_hour == shift_start_time[1]):
                    timetable[start_day][i][1:(active_shifts + 1)] = shifts
                    if active_shifts > 2:
                        timetable[start_day + 1][i][0] = 1
                elif (new_start_hour == shift_start_time[2]):
                    timetable[start_day][i][2] = 1
                    if active_shifts > 1:
                        timetable[start_day + 1][i][:active_shifts] = shifts
                            
        print(timetable)
        
        chain_need = [[],[],[]]
        with open(f"VM2C/{data_path}/02_dinh_bien.txt","r") as f:
            temp = [x.split() for x in f.readlines()]
            for x in temp:
                chain_need[int(x[0][-1])-1].append(int(x[2]))
        
        if chain_need[0] == []: chain_need[0] = np.zeros((3),dtype=int)
        if chain_need[1] == []: chain_need[1] = np.zeros((3),dtype=int)
        if chain_need[2] == []: chain_need[2] = np.zeros((3),dtype=int)

        return (id_to_code, skill, timetable, chain_need)
        
    def printInputIP(self,datapack):
        hash_table, skill, timetable, chain_need = self.readDatasetIP(datapack=datapack)
        with open("FormattedInput.txt","w") as f:
            f.write(str(len(hash_table)) + '\n')

            for axis1 in skill:
                for axis2 in axis1:
                    for val in axis2:
                        f.write(str(val) + ' ')
                    f.write('\n')
                f.write('\n')
            
            for row in chain_need:
                for val in row:
                    f.write(str(val) + ' ')
                f.write('\n')
            f.write('\n')

            for axis1 in timetable:
                for axis2 in axis1:
                    for val in axis2:
                        f.write(str(val) + ' ')
                    f.write('\n')
                f.write('\n')

            for k,v in hash_table.items():
                f.write(f"{k} {v}\n")

    def readDatasetFlow(self,datapack):
        if datapack == 1:
            num_folds = 1
            data_path = r"duLieu1"
        else:
            num_folds = 3
            data_path = r"duLieu2"
        staff = pd.read_csv(f"VM2C/{data_path}/01_nhan_su.txt", sep=" ")
        code_to_id = dict(zip(staff["ma_nhan_su"], staff["so_thu_tu"]) )
        id_to_code = dict(zip(staff["so_thu_tu"], staff["ma_nhan_su"]) )
        with open("Flow_FormattedInput.txt","w") as f :  
            f.write(f"{len(staff)}\n")
            f.write(f"{num_folds}\n")        
            for i in range(num_folds): 
                x = np.loadtxt(f"VM2C/{data_path}/ky_nang_Day_chuyen_{i+1}_Rot.txt",dtype ="str")
                f.write(str(len(x)) + ' ')
                for c in x:
                    if c[1] == '0':
                        f.write(c[2] + ' ')
                    else:
                        f.write(c[1:] + ' ')
                f.write('\n')  
                x = np.loadtxt(f"VM2C/{data_path}/ky_nang_Day_chuyen_{i+1}_May_dong_hop.txt",dtype ="str")
                f.write(str(len(x)) + ' ')
                for c in x:
                    if c[1] == '0':
                        f.write(c[2] + ' ')
                    else:
                        f.write(c[1:] + ' ')
                f.write('\n')  
                x = np.loadtxt(f"VM2C/{data_path}/ky_nang_Day_chuyen_{i+1}_Pallet.txt",dtype ="str")
                f.write(str(len(x)) + ' ')
                for c in x:
                    if c[1] == '0':
                        f.write(c[2] + ' ')
                    else:
                        f.write(c[1:] + ' ')
                f.write('\n')  
            
            with open(f"VM2C/{data_path}/02_dinh_bien.txt", "r") as finp:
                z = finp.readlines()
                for i in z:
                    f.write(i.split()[2] + '\n') 

            timetable = np.zeros( (29,3,3) ,dtype = int)
            
            def convert_to_start_time(_time):
                return 6 if 6 <= _time < 14 else 14 if 14 <= _time < 22 else 22

            def convert_to_end_time(_time):
                return 14 if 6 < _time <= 14 else 22 if 14 < _time <= 22 else 30
            
            for i in range(num_folds):
                with open(f"VM2C/{data_path}/lenh_san_xuat_Day_chuyen_{i+1}.txt","r") as fl:
                    fl.readline()  # Comment line
                    _time = [line.strip().split() for line in fl.readlines()]
                    
                    start_day = int(_time[i][0][8:10])
                    start_hour = int(_time[i][1][0:2])

                    end_day = int(_time[i][2][8:10])
                    end_hour = int(_time[i][3][0:2])

                    shift_start_time = [6, 14, 22]
                    
                    if (start_hour >= 0 and start_hour < shift_start_time[0]):
                        timetable[start_day - 1][i][2] = 1
                        continue
                    new_start_hour = convert_to_start_time(start_hour)
                    new_end_hour = convert_to_end_time(end_hour)
                    active_shifts = (new_end_hour - new_start_hour) // HOURS_PER_SHIFT
                    
                    shifts = [1] * active_shifts
                    if (new_start_hour == shift_start_time[0]):
                        timetable[start_day][i][:active_shifts] = shifts
                    elif (new_start_hour == shift_start_time[1]):
                        timetable[start_day][i][1:(active_shifts + 1)] = shifts
                        if active_shifts > 2:
                            timetable[start_day + 1][i][0] = 1
                    elif (new_start_hour == shift_start_time[2]):
                        timetable[start_day][i][2] = 1
                        if active_shifts > 1:
                            timetable[start_day + 1][i][:active_shifts] = shifts

            for i in range(1,29):
                for j in range(num_folds):
                    tmp = [x+1 for x in range(3) if timetable[i][j][x]]
                    f.write(str(len(tmp)) + ' ')
                    for z in tmp:
                        f.write(str(z) + ' ')
                    f.write('\n')  


def test():
    Reader = Readfile()
    Reader.readDatasetIP(datapack=1)
        

if __name__ == '__main__':
    test()
    
