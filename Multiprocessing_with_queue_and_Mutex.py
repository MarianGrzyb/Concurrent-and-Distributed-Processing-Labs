from multiprocessing import Process, Queue, Lock
import time
import os

NUMBER_OF_PROCESSORS = 10
MAX_NUMBER = 20000000
DECIMAL_PRECISION = 6
TIMEOUT = 10

def fun(n):
    print("(Sequential) Sum of all the calculations:", sum([x**2 for x in range(n)]))

def computation(startingNumber, endingNumber, r, l):
    totalPortion = 0
    print("Process ID:", os.getpid(), "| Processing range:", startingNumber, "-", endingNumber)
    for x in range(startingNumber, endingNumber):
        totalPortion += x**2

    l.acquire()
    try:
        r.put(totalPortion)
    finally:
        l.release()

if __name__ == "__main__":
    start_time = time.time()
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

    end_time = time.time()
    total_time_parallel = round(end_time - start_time, DECIMAL_PRECISION)

    print("Number of logical processors:", os.cpu_count())
    print("Processors used for calculations:", NUMBER_OF_PROCESSORS)
    print("(Parallel) Sum of all the calculations:", total)
    print("(Parallel) Total time taken:", total_time_parallel, "seconds")

    start_time = time.time()
    fun(MAX_NUMBER)
    end_time = time.time()
    total_time_sequential = round(end_time - start_time, DECIMAL_PRECISION)

    print("(Sequential) Total time taken:", total_time_sequential, "seconds")
