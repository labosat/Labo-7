from k2612B import run
from functions import P

#script for saving secuential measurements automatically for k2612B and k2400
#optimal values for 'iv': N = 50, wait_time = 0.01

N = 50
wait_time = 0.01
group_path = 'Estacionario Full integration'

#modes available: 'iv', 'led1', 'led2' (refer to help for specifics)
mode = 'iv'

plotFlag = 1
saveFlag = 0

for j in range(1, N + 1):
    run(j, mode, group_path, plotFlag, saveFlag, wait_time)
    
    
#%% script for saving data with different wait times in 'iv' mode
from k2612B import run
from functions import P

    
group_path = 'Wait Time Multiple (rq)'
wait_time = [100*P('n'), 1*P('u'), 10*P('u'), 100*P('u'), 1*P('m'), 10*P('m'), 25*P('m'), 50*P('m'), 75*P('m'), 100*P('m')]
folders = ["1e-7", "1e-6", "1e-5", "0.0001", "0.001", "0.01", "0.025", "0.05", "0.075", "0.1"]
N = 15

plotFlag = 1
saveFlag = 1

for j in range(0, N):
    index = j + 1
    path0 = '/' + str(folders[0])
    run(index, 'iv', group_path + path0, plotFlag, saveFlag, wait_time[0])
    
    path1 = '/' + str(folders[1])
    run(index, 'iv', group_path + path1, plotFlag, saveFlag, wait_time[1])
    
    path2 = '/' + str(folders[2])
    run(index, 'iv', group_path + path2, plotFlag, saveFlag, wait_time[2])
    
    path3 = '/' + str(folders[3])
    run(index, 'iv', group_path + path3, plotFlag, saveFlag, wait_time[3])
    
    path4 = '/' + str(folders[4])
    run(index, 'iv', group_path + path4, plotFlag, saveFlag, wait_time[4])
    
    path5 = '/' + str(folders[5])
    run(index, 'iv', group_path + path5, plotFlag, saveFlag, wait_time[5])
    
    path6 = '/' + str(folders[6])
    run(index, 'iv', group_path + path6, plotFlag, saveFlag, wait_time[6])
    
    path7 = '/' + str(folders[7])
    run(index, 'iv', group_path + path7, plotFlag, saveFlag, wait_time[7])
    
    path8 = '/' + str(folders[8])
    run(index, 'iv', group_path + path8, plotFlag, saveFlag, wait_time[8])
    
    path9 = '/' + str(folders[9])
    run(index, 'iv', group_path + path9, plotFlag, saveFlag, wait_time[9])

    
    print(str(j) + " successful!")