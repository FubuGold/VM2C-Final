import numpy as np 
import matplotlib.pyplot as plt 
import statistics as stats
def Load_Result(data_pack,part,method): 
    method = method 
    print(method)
    part = part 
    n = 0 
    if(data_pack == 2) : 
       n = 55
    if(data_pack == 1): 
       n =  17 
    if method == "IP":
        path = f'result_data_{data_pack}_part_{part}.txt'  
    else:
        path = f'result_data_{data_pack}_part_{part}_{method}.txt'  
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
                check_list[id-1][0] += 1 
                check_list[id-1][1] += 1 
    np.savetxt(f"Balance_result_{data_pack}_part_{part}_{method}",check_list.astype(int),fmt='%d')
def Balance(balance) : 
      value = []
      night_shift = [ ]
      for i in range(len(balance)) : 
        value.append(balance[i][0])
        night_shift.append(balance[i][1])
      return value,night_shift
def calculate_standard_deviation(data):
    n = len(data)
    
    mean = sum(data) / n
    
    # Step 2: Calculate the squared differences between data points and the mean
    squared_diff = [(x - mean) ** 2 for x in data]
    
    # Step 3: Calculate the mean of the squared differences
    mean_squared_diff = sum(squared_diff) / n
    
    # Step 4: Take the square root to get the standard deviation
    standard_deviation = mean_squared_diff ** 0.5
    
    return standard_deviation
if __name__ == "__main__":
    part = "b"
    method = "IP"
    datapack = 2
    Load_Result(datapack,part = part,method = method)
    balance = np.loadtxt(f"Balance_result_{datapack}_part_{part}_{method}")
    balance = balance[~(balance == 0).all(axis=1)]
    print(balance.shape)
    value,night_shift = Balance(balance)

    print(stats.stdev(night_shift))
    print(stats.stdev(value))
    plt.plot([], [], ' ', label=f'Total_workers = {len(value)}')
    plt.hist(night_shift,label = "night_shift")
    plt.hist(value,label = "total_shift")
    plt.xticks([i for i in range(30)])
    plt.subplot
    plt.legend()
    plt.savefig(f'result_{datapack}_part_{part}_{method}.png')
    plt.show()  
    