import numpy as np 
def Load_Result(data_path): 
    n = 55
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
if __name__ == "__main__": 
    Load_Result(data_path=2)