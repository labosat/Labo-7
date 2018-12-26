from k2612B import run
import time

N          = 3
group_path = 'Encapsulado 1\\5'
test       = ['iv', 'self_heating']
plotFlag   = 1
saveFlag   = 1

for i in range(1, N + 1):
    print(str(i))
    run(i, test[0], group_path, plotFlag, saveFlag)
    time.sleep(0)