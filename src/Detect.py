from IPlist import IPList
from math import log
import time
start_time = time.time()



detectionDelay = 2
attackCount = 0

def init():
    IPlist = IPList()
    for currentTime in AddFlow(IPlist):
        CountAndDelete(IPlist, currentTime)
        print(currentTime)
    CountAndDelete(IPlist, currentTime+detectionDelay)
    print(currentTime+detectionDelay)
    
def AddFlow(IPlist):

    currentTime = 0
    
    try:
        file = open('test3.csv', 'r')
        for line in file.readlines():
            added = IPlist.add(line.strip(), currentTime, detectionDelay)
            while(not added):
                currentTime += detectionDelay
                yield currentTime
                added = IPlist.add(line.strip(), currentTime, detectionDelay)
    except IOError:
        print("not found")
#     print(SYNcount, PcktCount, IPlist)
    print(IPlist)
    
def CountAndDelete(IPlist, currentTime):
    removedSockets = IPlist.remove(currentTime)

    
    #calculate ratio
    ratio = 0
    sum = IPlist.p1 + IPlist.p2 + IPlist.p3 + IPlist.p4
    if IPlist.pcktCount > 0 :
        ratio = (sum/IPlist.pcktCount)
#     print(IPlist.pcktCount, sum, percentage)
        print("Ratio = ", ratio)
    if ratio > 0.3 :
        print("Potential Attack Detected \nSwitching into safe mode")
        #print(removedSockets)
        global attackCount 
        attackCount += 1
        




init()
print(attackCount)
print("--- %s seconds ---" % (time.time() - start_time))

