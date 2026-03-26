from multiprocessing import Process, Queue, Lock
import time

NUMBER_OF_PROCESSORS = 10
MAX_NUMBER = 20000000
DECIMAL_PRECISION = 6
TIMEOUT = 10

def computation(startingNumber, endingNumber, r, l):
    totalPortion = 0
    #print("Process ID:", os.getpid(), "| Processing range:", startingNumber, "-", endingNumber)
    for x in range(startingNumber, endingNumber):
        totalPortion += x**2

    l.acquire()
    try:
        r.put(totalPortion)
    finally:
        l.release()

def queue():
    startTime = time.time()
    sharedResource = Queue()
    lock = Lock()
    processes = []

    for processId in range(0, NUMBER_OF_PROCESSORS):
        portionForWorker = int(MAX_NUMBER / NUMBER_OF_PROCESSORS)
        bottomThreshold = processId * portionForWorker
        upperThreshold = (processId + 1) * portionForWorker
        if upperThreshold != 0:
            processes.append(Process(target = computation, args = (bottomThreshold, upperThreshold, sharedResource, lock)))

    for process in processes:
        process.start()

    finishedOnTime = 0

    for process in processes:
        process.join(timeout = TIMEOUT)

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
    totalTimeParallel = round(endTime - startTime, DECIMAL_PRECISION)

    return totalTimeParallel
