from run import fun
from Multiprocessing_with_queue_and_Mutex import queue

from multiprocessing import Process, Array, Semaphore
import time

NUMBER_OF_PROCESSORS = 10
MAX_NUMBER = 20000000
NUMBER_OF_SEMAPHORES = 1
EMPTY_FIELD = -1
TIMEOUT = 10
DECIMAL_PRECISION = 6
NUMBER_OF_ITERATIONS = 20

def computation(minimum, maximum, sharedMemory, s):
    #print("Process ID:", os.getpid(), "| Processing range:", minimum, "-", maximum)
    partialSum = 0

    for x in range(minimum, maximum):
        partialSum += x ** 2

    with s:
        try:
            for index in range(len(sharedMemory)):
                if sharedMemory[index] == EMPTY_FIELD:
                    sharedMemory[index] = partialSum
                    break
        except Exception as e:
            print("Exception:", e)

def arrayparallel():
    startTime = time.time()
    portion = int(MAX_NUMBER / NUMBER_OF_PROCESSORS)
    processes = []
    array = Array('d', [EMPTY_FIELD] * NUMBER_OF_PROCESSORS)
    semaphore = Semaphore(NUMBER_OF_SEMAPHORES)

    for process in range(NUMBER_OF_PROCESSORS):
        lowerThreshold = process * portion
        upperThreshold = (process + 1) * portion

        if upperThreshold == 0:
            raise Exception('upper threshold cannot be zero')
        else:
            processes.append(Process(target=computation, args=(lowerThreshold, upperThreshold, array, semaphore)))

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

    for element in range(len(array)):
        total += array[element]

    endTime = time.time()
    totalTime = round(endTime - startTime, DECIMAL_PRECISION)

    return totalTime, total

if __name__ == "__main__":
    totalTimeArrayTest, totalArray = arrayparallel()
    print("(Array) Sum of all the calculations:", totalArray)
    print("(Array) Total time taken:", totalTimeArrayTest, "seconds")

    startTimeSequential = time.time()
    fun(MAX_NUMBER)
    endTimeSequential = time.time()
    totalTimeSequential = round(endTimeSequential - startTimeSequential, DECIMAL_PRECISION)

    print("(Sequential) Total time taken:", totalTimeSequential, "seconds")

    totalTimeQueue = 0
    tMaxQueue = 0
    tMinQueue = 100000

    for i in range(NUMBER_OF_ITERATIONS):
        singleMeasurementQueue = queue()
        totalTimeQueue += singleMeasurementQueue

        if singleMeasurementQueue > tMaxQueue:
            tMaxQueue = singleMeasurementQueue

        if singleMeasurementQueue < tMinQueue:
            tMinQueue = singleMeasurementQueue

    print("(Queue) Mean:", totalTimeQueue / NUMBER_OF_ITERATIONS)
    print("(Queue) Max: ", tMaxQueue)
    print("(Queue) Min", tMinQueue)
    print("(Queue) Uncertainty:", round((tMaxQueue - tMinQueue) / 2, DECIMAL_PRECISION))

    totalTimeArray = 0
    tMaxArray = 0
    tMinArray = 100000

    for i in range(NUMBER_OF_ITERATIONS):
        singleMeasurementArray, _ = arrayparallel()
        totalTimeArray += singleMeasurementArray

        if singleMeasurementArray > tMaxArray:
            tMaxArray = singleMeasurementArray

        if singleMeasurementArray < tMinArray:
            tMinArray = singleMeasurementArray

    print("(Array) Mean:", totalTimeArray / NUMBER_OF_ITERATIONS)
    print("(Array) Max: ", tMaxArray)
    print("(Array) Min", tMinArray)
    print("(Array) Uncertainty:", round((tMaxArray - tMinArray) / 2, DECIMAL_PRECISION))
