import gurobipy
import gurobipy as gp  # import the installed package
from gurobipy import GRB
params = {
"WLSACCESSID": 'f164f691-1d84-4092-a810-e324efa273f0',
"WLSSECRET": '52be21e1-ad4a-439a-9963-1d8af268ab0e',
"LICENSEID": 2395694,
}
env = gp.Env(params=params)

# Create the model within the Gurobi environment
model = gp.Model(env=env)

import pandas as pd 
import numpy as np 
staff = pd.read_csv("staff.txt", sep=" ")
rot = np.loadtxt("Rot_availability.txt",dtype ="str")
pallet = np.loadtxt("Pallet1_availability.txt",dtype ="str")
compressor = np.loadtxt("Compressor_availability.txt",dtype ="str")