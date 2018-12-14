from k2612B import run
import time

N = 1
group_path = 'Medicion PID'
plotFlag = 1
saveFlag = 1

for i in range(1, N + 1):
    print(str(i))
    run(i, group_path, plotFlag, saveFlag)
#    time.sleep(60)


