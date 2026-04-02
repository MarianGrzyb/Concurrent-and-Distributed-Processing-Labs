from multiprocessing import Process, Queue, Lock
import time

def computation(startingNumber, endingNumber, r, l):
    totalPortion = 0
    for x in range(startingNumber, endingNumber):
        totalPortion += x**2

    l.acquire()
    try:
        r.put(totalPortion)
    finally:
        l.release()

def queue(maxNumber, NumberOfProcessors, timeout, decimalPrecision):
    startTime = time.time()
    portionForWorker = int(maxNumber / NumberOfProcessors)
    processes = []
    sharedResource = Queue()
    lock = Lock()

    for processId in range(0, NumberOfProcessors):
        bottomThreshold = processId * portionForWorker
        upperThreshold = (processId + 1) * portionForWorker
        if upperThreshold != 0:
            processes.append(Process(target = computation, args = (bottomThreshold, upperThreshold, sharedResource, lock)))

    for process in processes:
        process.start()

    finishedOnTime = 0

    for process in processes:
        process.join(timeout = timeout)

        if process.is_alive():
            print("Process hasn't finished yet!")
            process.terminate()
            process.join()
        else:
            finishedOnTime += 1

    total = 0
    for resource in range(0, finishedOnTime):
        total += sharedResource.get()

    endTime = time.time()
    totalTime = round(endTime - startTime, decimalPrecision)

    return totalTime
