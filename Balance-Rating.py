import numpy as np 
import matplotlib.pyplot as plt 
def Load_Result(data_path): 
    n = 0 
    if(data_path == 2) : 
       n = 55
    if(data_path == 1): 
       n =  17 
    path = f'result_data_{data_path}_part_a.txt'  
    check_list = np.zeros((n,2),dtype=int)
    with open(path,"r") as f : 
        z = f.readlines()
        for i in range(len(z)) : 
            k = z[i].split()
            y = int(k[1][-1])
            id = int(k[2][1:])
            if(y <= 2 ) : 
                check_list[id-1][0] += 1  
            else : 
                check_list[id-1][1] += 1 
    np.savetxt(f"Balance_Result_{data_path}_part_a",check_list.astype(int),fmt='%d')
def Balance(balance) : 
      value = []
      for i in range(len(balance)) : 
        value.append(balance[i][0] + balance[i][1])
      return value
if __name__ == "__main__": 
    Load_Result(2)
    balance = np.loadtxt("Balance_Result_2_part_a")
    value = Balance(balance)
    plt.hist(value)
    plt.show()