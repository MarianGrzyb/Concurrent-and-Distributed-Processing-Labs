from multiprocessing import Process, Array, Semaphore
import time

NUMBER_OF_SEMAPHORES = 1
EMPTY_FIELD = -1

def computation(minimum, maximum, sharedMemory, s):
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

def arrayparallel(maxNumber, numberOfProcessors, timeout, decimalPrecision):
    startTime = time.time()
    portion = int(maxNumber / numberOfProcessors)
    processes = []
    array = Array('d', [EMPTY_FIELD] * numberOfProcessors)
    semaphore = Semaphore(NUMBER_OF_SEMAPHORES)

    for process in range(numberOfProcessors):
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
        process.join(timeout = timeout)

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
    totalTime = round(endTime - startTime, decimalPrecision)

    return totalTime, total
