from multiprocessing import Process, Queue
import random
import time

POISON_PILL = -1
TIMEOUT_DURATION = 3
NUMBER_OF_LINES = 100
MIN_NUMBER = 0
MAX_NUMBER = 100

def fileInit(file):
    with open(file, "w") as f:
        for i in range(NUMBER_OF_LINES):
            f.write(str(random.randint(MIN_NUMBER, MAX_NUMBER)) + "\n")

def readFromFile(file, queue):
    firstArray = []
    secondArray = []

    with open(file, "r") as f:
        for line in f:
            if random.randint(0, 1) != 0:
                firstArray.append(int(line.strip()))
            else:
                secondArray.append(int(line.strip()))

    queue.put(firstArray)
    queue.put(secondArray)
    queue.put(POISON_PILL)
    queue.put(POISON_PILL)


def sortarray(inputStructure, outputStructure):
    while True:
        if not inputStructure.empty():
            inputValue = inputStructure.get(timeout = TIMEOUT_DURATION)

            if inputValue != POISON_PILL:
                inputValue.sort()
                outputStructure.put(inputValue)
            else:
                break
        else:
            break


if __name__ == "__main__":
    fileName = "file.txt"
    fileInit(fileName)

    inputQueue = Queue()
    outputQueue = Queue()

    start = time.time()
    readFromFile(fileName, inputQueue)

    childProcess1 = Process(target=sortarray, args=(inputQueue, outputQueue))
    childProcess2 = Process(target=sortarray, args=(inputQueue, outputQueue))

    childProcess1.start()
    childProcess2.start()

    childProcess1.join()
    childProcess2.join()

    arrayToMerge = []

    while not outputQueue.empty():
        array = outputQueue.get()

        for i in array:
            arrayToMerge.append(i)

    mergedArray = sorted(arrayToMerge)
    print("Full array sorted:", mergedArray)

    end = time.time()
    print("Time taken:", round(end - start, 6))
