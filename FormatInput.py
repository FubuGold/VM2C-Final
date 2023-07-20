import os
import numpy as np
import pandas as pd
class Readfile:

    daychuyen_code_to_id = {'Day_chuyen_1' : 0, 'Day_chuyen_2' : 1,'Day_chuyen_3' : 2}
    skill_to_id = {"Rot" : 0, "Pallet" : 1, "May_dong_hop" : 2}

    def __init__(self):
        pass

    def readDataset1(self):
        staff = pd.read_csv("VM2C/duLieu1/staff.txt", sep=" ")
        staff["so_thu_tu"] = staff["so_thu_tu"].apply(lambda x : x - 1)
        code_to_id = dict(zip(staff["ma_nhan_su"], staff["so_thu_tu"]) )
        id_to_code = dict(zip(staff["so_thu_tu"], staff["ma_nhan_su"]) )

        skill = np.zeros(shape = (len(code_to_id), 3) , dtype = int)

        # rot = 0, pallet = 1, compressor = 2
        rot = np.loadtxt("VM2C/duLieu1/Rot_availability.txt",dtype ="str")
        for nhan_vien in rot:
            id = code_to_id[nhan_vien] 
            skill[id,0] = 1
        
        pallet = np.loadtxt("VM2C/duLieu1/Pallet1_availability.txt",dtype ="str")
        for nhan_vien in pallet:
            id = code_to_id[nhan_vien]
            skill[id,1] = 1

        compressor = np.loadtxt("VM2C/duLieu1/Compressor_availability.txt",dtype ="str")
        for nhan_vien in compressor:
            id = code_to_id[nhan_vien]
            skill[id,2] = 1

        timetable = np.zeros( (29,3,3) ,dtype = int)
                                # Ngay Day-Chuyen Ca

        with open("VM2C/duLieu1/Command-1.txt","r") as f:
            com = f.readlines()
            for time in com:
                time = time.split()
                if len(time) != 4: continue
                day = int(time[0][-2:])
                next_day = int(time[2][-2:])
                if time[1] < "06:00:00":
                    timetable[day-1][0][2] = 1
                if time[1] <= "14:00:00":
                    timetable[day][0][0] = 1
                if next_day > day or time[3] > "22:00:00":
                    timetable[day][0][2] = 1
                if time[1] <= "22:00:00":
                    timetable[day][0][1] = 1
        
        return (id_to_code, skill, timetable)
        
        
    def readDataset2(self):
        ...
        
def PrintInput():
    Reader = Readfile()
    hash_table, skill, timetable = Reader.readDataset1()
    with open("FormattedInput.txt","w") as f:
        f.write(str(len(hash_table)) + '\n')
        for row in skill:
            for val in row:
                f.write(str(val) + ' ')
            f.write("\n")
        f.write('\n')
        for axis1 in timetable:
            for axis2 in axis1:
                for val in axis2:
                    f.write(str(val) + ' ')
                f.write('\n')
            f.write('\n')

        
        

if __name__ == '__main__':
    PrintInput()