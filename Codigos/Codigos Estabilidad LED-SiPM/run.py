from k2612B import run
from functions import P
import time

#script for saving secuential measurements automatically for k2612B and k2400
#optimal values for 'iv': N = 50, wait_time = 0.01
#                   'led1': N = 50, wait_time < 0.01
#                   'led2': N = 1, wait_time = 0.01, measurements = 10000
#                    (total time of measurement would be 100s)
#                   'led3': N = 50, wait_time = 0.01

N = 1
wait_time = 6*P('m')
group_path = 'Auto calentamiento, dt = 6ms, NPLC = 0.1, espera 10s, datos=6 BIS'

#modes available: 'iv', 'led1', 'led2' (refer to help for specifics)
mode = 'led1'
NPLC = 0.001
iPolarization_led = "none"

plotFlag = 1
saveFlag = 0

for j in range(1, N + 1):
    run(j, mode, group_path, plotFlag, saveFlag, wait_time, NPLC, iPolarization_led)
    #time.sleep(10)

#%%  # ESTA FUNCION ES PARA MEDIR UNA CURVA ISIPM ILED EN FUNCION DEL WAIT TIME.
from k2612B import run
from functions import P
import time  

wait_time = [1e-7, 1e-6, 1e-5, 0.0001, 0.001, 0.01, 0.025, 0.05, 0.075, 0.1]

N = 1
group_path = ["1e-7", "1e-6", "1e-5", "0.0001", "0.001", "0.01", "0.025", "0.05", "0.075", "0.1"]

#modes available: 'iv', 'led1', 'led2' (refer to help for specifics)
mode = 'led1'
NPLC = 1
iPolarization_led = "none"

plotFlag = 1
saveFlag = 1

for j in range(len(wait_time)):
    run(1, mode, group_path[j], plotFlag, saveFlag, wait_time[j], NPLC, iPolarization_led)
    time.sleep(60)
    
    
#%%
from k2612B import run
from functions import P
import time   

#run this code to get noise in sipm current as a function of time for
#different led currents and integration times

N = 1
measurements = 100
path_name = 'Estacionario 8'

folders = ["0.01 NPLC", "0.1 NPLC", "1 NPLC"]
mode = 'led2'
plotFlag = 1
saveFlag = 1

wait_time = 10*P('m')
NPLC = [0.01, 0.1, 1]
time_sleep = [(5+wait_time+((NPLC[i]/50.)*measurements)) for i in range(len(NPLC))]

startTime = time.time()
for iPolarization_led in [1*P('m'), 5*P('m'), 10*P('m'), 15*P('m'), 20*P('m')]:
    
    for i in range(0, len(folders)):
        run(1, mode, path_name + '//' +  folders[i] + '//' + str(iPolarization_led) + "A", plotFlag, saveFlag, wait_time, NPLC[i], iPolarization_led)
        time.sleep(int(time_sleep[i]))
    
elapsed = time.time() - startTime
print(elapsed)

#%%
from k2612B import run
from functions import P
import time

#run this code to get iv curve on sipm for different fixed led currents

N = 1
path_name = 'Estacionario 7'
    
mode = 'led3'
wait_time = 10*P('m')
NPLC = 1
plotFlag = 1
saveFlag = 1

startTime = time.time()
for iPolarization_led in [1*P('m'), 5*P('m'), 10*P('m'), 15*P('m'), 20*P('m'), 25*P('m'), 50*P('m'), 75*P('m'), 100*P('m'), 125*P('m'), 150*P('m'), 175*P('m')]:
    
    run(1, mode, path_name + '//' + str(iPolarization_led) + "A" , plotFlag, saveFlag, wait_time, NPLC, iPolarization_led)
    time.sleep(iPolarization_led*200)
    
    if iPolarization_led == 0.2:
        break
    
    if iPolarization_led >= 0.020:
        time.sleep(500*iPolarization_led)
        
    
    
elapsed = time.time() - startTime
print(elapsed)


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