from run import fun
from Multiprocessing_with_queue_and_Mutex import queue
from Multiprocessing_with_shared_memory_and_semaphore import arrayparallel

from multiprocessing import Process, Pipe, Value, Condition, RLock
import time

NUMBER_OF_PROCESSORS = 10
MAX_NUMBER = 20000000
TIMEOUT = 10
DECIMAL_PRECISION = 6
NUMBER_OF_ITERATIONS = 50
MAX_TIME = 0
MIN_TIME = 10000

def computation(minimum, maximum, connection, condition, counter):
    partialSum = 0

    for x in range(minimum, maximum):
        partialSum += x ** 2

    try:
        connection.send(partialSum)
    except Exception as e:
        print("Exception:", e)
    connection.close()

    with condition:
        counter.value += 1
        condition.notify_all()

def pipe(maxNumber, NumberOfProcessors, timeout, decimalPrecision):
    startTime = time.time()
    portion = int(maxNumber / NumberOfProcessors)
    processes = []
    receivers = []
    globalCounter = Value('i', 0)
    cond = Condition()

    for process in range(NumberOfProcessors):
        parentConnection, childConnection = Pipe(duplex=False)
        lowerThreshold = process * portion
        upperThreshold = (process + 1) * portion

        if upperThreshold == 0:
            raise Exception('upper threshold cannot be zero')
        else:
            processes.append(Process(target=computation, args=(lowerThreshold, upperThreshold, childConnection, cond, globalCounter)))
            receivers.append(parentConnection)

    for process in processes:
        process.start()

    with cond:
        while globalCounter.value < NUMBER_OF_PROCESSORS:
            break

    total = 0

    for connection in receivers:
        try:
            if connection.poll(timeout):
                total += connection.recv()
            else:
                print("Waiting for data!")
        except Exception as e:
            print("Exception:", e)
        connection.close()

    finishedOnTime = 0

    for process in processes:
        process.join(timeout = timeout)

        if process.is_alive():
            print("Process hasn't finished yet!")
            process.terminate()
            process.join()
        else:
            finishedOnTime += 1

    endTime = time.time()
    totalTime = round(endTime - startTime, decimalPrecision)

    return totalTime, total

if __name__ == "__main__":
    totalTimePipeTest, totalPipe = pipe(MAX_NUMBER, NUMBER_OF_PROCESSORS, TIMEOUT, DECIMAL_PRECISION)
    print("(Pipe) Sum of all the calculations:", totalPipe)
    print("(Pipe) Total time taken:", totalTimePipeTest, "seconds")

    startTimeSequential = time.time()
    fun(MAX_NUMBER)
    endTimeSequential = time.time()
    totalTimeSequential = round(endTimeSequential - startTimeSequential, DECIMAL_PRECISION)

    print("(Sequential) Total time taken:", totalTimeSequential, "seconds")

    totalTimeQueue = 0
    tMaxQueue = MAX_TIME
    tMinQueue = MIN_TIME

    for i in range(NUMBER_OF_ITERATIONS):
        singleMeasurementQueue = queue(MAX_NUMBER, NUMBER_OF_PROCESSORS, TIMEOUT, DECIMAL_PRECISION)
        totalTimeQueue += singleMeasurementQueue

        if singleMeasurementQueue > tMaxQueue:
            tMaxQueue = singleMeasurementQueue

        if singleMeasurementQueue < tMinQueue:
            tMinQueue = singleMeasurementQueue

    print("(Queue) Mean:", totalTimeQueue / NUMBER_OF_ITERATIONS)
    print("(Queue) Uncertainty:", round((tMaxQueue - tMinQueue) / 2, DECIMAL_PRECISION))

    totalTimeArray = 0
    tMaxArray = MAX_TIME
    tMinArray = MIN_TIME

    for i in range(NUMBER_OF_ITERATIONS):
        singleMeasurementArray, _ = arrayparallel(MAX_NUMBER, NUMBER_OF_PROCESSORS, TIMEOUT, DECIMAL_PRECISION)
        totalTimeArray += singleMeasurementArray

        if singleMeasurementArray > tMaxArray:
            tMaxArray = singleMeasurementArray

        if singleMeasurementArray < tMinArray:
            tMinArray = singleMeasurementArray

    print("(Array) Mean:", totalTimeArray / NUMBER_OF_ITERATIONS)
    print("(Array) Uncertainty:", round((tMaxArray - tMinArray) / 2, DECIMAL_PRECISION))

    totalTimePipe = 0
    tMaxPipe = MAX_TIME
    tMinPipe = MIN_TIME

    for i in range(NUMBER_OF_ITERATIONS):
        singleMeasurementPipe, _ = pipe(MAX_NUMBER, NUMBER_OF_PROCESSORS, TIMEOUT, DECIMAL_PRECISION)
        totalTimePipe += singleMeasurementPipe

        if singleMeasurementPipe > tMaxPipe:
            tMaxPipe = singleMeasurementPipe

        if singleMeasurementPipe < tMinPipe:
            tMinPipe = singleMeasurementPipe

    print("(Pipe) Mean:", totalTimePipe / NUMBER_OF_ITERATIONS)
    print("(Pipe) Uncertainty:", round((tMaxPipe - tMinPipe) / 2, DECIMAL_PRECISION))
