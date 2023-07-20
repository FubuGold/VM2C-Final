import os
import numpy as np
import pandas as pd
command =pd.read_csv("VM2C/duLieu1/Command-1.txt",sep = "; ")
class Readfile:

    daychuyen_code_to_id = {'Day_chuyen_1' : 0, 'Day_chuyen_2' : 1,'Day_chuyen_3' : 2}
    skill_to_id = {"Rot" : 0, "Pallet" : 1, "May_dong_hop" : 2}

    def readDataset1(self):
        staff = pd.read_csv("../VM2C/duLieu1/staff.txt", sep=" ")
        staff["so_thu_tu"] = staff["so_thu_tu"].apply(lambda x : x - 1)
        self.code_to_id = dict(zip(staff["ma_nhan_su"], staff["so_thu_tu"]) )
        self.id_to_code = dict(zip(staff["so_thu_tu"], staff["ma_nhan_su"]) )

        self.skill = np.zeros(shape = (len(self.code_to_id), 3) , dtype = bool)

        # rot = 0, pallet = 1, compressor = 2
        rot = np.loadtxt("../VM2C/duLieu1/Rot_availability.txt",dtype ="str")
        for nhan_vien in rot:
            id = self.code_to_id[nhan_vien] 
            self.skill[id,0] = 1
        
        pallet = np.loadtxt("../VM2C/duLieu1/Pallet1_availability.txt",dtype ="str")
        for nhan_vien in pallet:
            id = self.code_to_id[nhan_vien]
            self.skill[id,2] = 1

        compressor = np.loadtxt("../VM2C/duLieu1/Compressor_availability.txt",dtype ="str")
        for nhan_vien in compressor:
            id = self.code_to_id[nhan_vien]
            self.skill[id,3] = 1
        
    def readDataset2(self):
        ...
    