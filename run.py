import time
# Exception to do: n not equal 0

def fun(n):
    print("(Sequential) Sum of all the calculations:", sum([x**2 for x in range(n)]))

if __name__ == "__main__":
    # Single processor
    fun(20000000)

#Remember to split the calculations
    # between processes in "multiprocessor" versions,
    # e.g. if you have four processors
    # processor 1: calculates function myFun() in range 1 to 5000000
    # processor 2: calculates function myFun() in range 5000000 to 10000000
    # processor 3: calculates function myFun() in range 10000000 to 15000000
    # processor 4: calculates function myFun() in range 15000000 to 20000000
    #
    # Calculate the final sum (the sum of the results from all processors)
    # in critical section.
