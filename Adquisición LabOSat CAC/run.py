from k2612B import run
import time
#import winsound

N          = 1
group_path = 'test'
test       = ['LabOSat']
plotFlag   = 1
saveFlag   = 1

for i in range(1, N + 1):
    print(str(i))
    run(i, test[0], group_path, plotFlag, saveFlag)
    time.sleep(0)

#winsound.Beep(750, 750)
#winsound.Beep(750, 750)
#winsound.Beep(750, 750)
#winsound.Beep(1000, 1000)
