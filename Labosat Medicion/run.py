from k2612B import run
import time

N = 25
group_path = 'Mediciones autocalentamiento 4'
plotFlag = 1
saveFlag = 1

for i in range(1, N + 1):
    run(i, group_path, plotFlag, saveFlag)
    time.sleep(30)


