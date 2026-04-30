from multiprocessing import Process, Pipe
import random
import time

FIRST_CHILD_ID = 0
SECOND_CHILD_ID = 1
NUMBER_OF_LINES = 200
MIN_NUMBER = 0
MAX_NUMBER = 100

def fileInit(file):
    with open(file, "w") as f:
        for i in range(NUMBER_OF_LINES):
            f.write(str(random.randint(MIN_NUMBER, MAX_NUMBER)) + "\n")

def readFromFile(file, conn1, conn2):
    firstArray = []
    secondArray = []

    with open(file, "r") as f:
        for line in f:
            if random.randint(0, 1) != 0:
                firstArray.append(int(line.strip()))
            else:
                secondArray.append(int(line.strip()))

    conn1.send(firstArray)
    conn1.close()
    conn2.send(secondArray)
    conn2.close()

def sortArray(receiver, sender):
    while not receiver.poll(0.1):
        pass
    array = receiver.recv()
    array.sort()
    sender.send(array)
    sender.close()

if __name__ == "__main__":
    fileName = "file.txt"
    fileInit(fileName)

    parentConnection1, childConnection1 = Pipe()
    parentConnection2, childConnection2 = Pipe()
    childConnection1Return, parentConnection1Return = Pipe()
    childConnection2Return, parentConnection2Return = Pipe()

    start = time.time()
    readFromFile(fileName, parentConnection1, parentConnection2)

    childProcess1 = Process(target=sortArray, args=(childConnection1, childConnection1Return))
    childProcess2 = Process(target=sortArray, args=(childConnection2, childConnection2Return))

    childProcess1.start()
    childProcess2.start()

    childProcess1.join()
    childProcess2.join()

    while not parentConnection1Return.poll(0.1):
        pass
    sortedArray1 = parentConnection1Return.recv()
    while not parentConnection2Return.poll(0.1):
        pass
    sortedArray2 = parentConnection2Return.recv()

    mergedArray = sorted(sortedArray1 + sortedArray2)
    print("Full array sorted:", mergedArray)

    end = time.time()
    print("Time taken:", round(end - start, 6))
