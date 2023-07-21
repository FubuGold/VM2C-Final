import os
import numpy as np
import pandas as pd
class Readfile:

    daychuyen_code_to_id = {'Day_chuyen_1' : 0, 'Day_chuyen_2' : 1,'Day_chuyen_3' : 2}
    skill_to_id = {"Rot" : 0, "May_dong_hop" : 1, "Pallet" : 2}
    

    def __init__(self):
        pass

    def readDataset1(self):
        data_path_1 = r"duLieu1"
        data_path_2 = r"duLieu2"
        num_folds = 1
        data_path = data_path_1
        
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


         with open(f"VM2C/{data_path}/lenh_san_xuat_Day_chuyen_{i+1}.txt","r") as f:
            com = f.readlines()
            for time in com:
                time = time.split()
                if len(time) != 4: continue
                day = int(time[0][-2:])
                next_day = int(time[2][-2:])
                if time[1] < "06:00:00":
                    timetable[day-1][i][2] = 1
                if time[1] <= "14:00:00":
                    timetable[day][i][0] = 1
                if next_day > day or time[3] > "22:00:00":
                    timetable[day][i][2] = 1
                if time[1] <= "22:00:00":
                    timetable[day][i][1] = 1
        
        chain_need = [[],[0,0,0],[0,0,0]]
        with open(f"VM2C/{data_path}/02_dinh_bien.txt","r") as f:
            temp = [x.split() for x in f.readlines()]
            for x in temp:
                chain_need[0].append(int(x[2]))
        
        return (id_to_code, skill, timetable, chain_need)
        
    def PrintInput1(self):
        hash_table, skill, timetable, chain_need = self.readDataset1()
        with open("FormattedInput.txt","w") as f:
            f.write(str(len(hash_table)) + ' 1\n')
        
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

def test():
    Reader = Readfile()
    Reader.PrintInput1()
        

if __name__ == '__main__':
    test()