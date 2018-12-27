from k2612B import run
import time
import winsound

N          = 5
group_path = 'Encapsulado 1 con grasa\\3'
test       = ['iv', 'self_heating']
plotFlag   = 1
saveFlag   = 1

for i in range(1, N + 1):
    print(str(i))
    run(i, test[0], group_path, plotFlag, saveFlag)
    time.sleep(0)

winsound.Beep(750, 750)
winsound.Beep(750, 750)
winsound.Beep(750, 750)
