import random
import time

def seq_search(l, target):
    for i in range(len (l)):
        if l[i] == target:
            return i
    else:
        return ("Not Found")

def binary_search(l, target, low = None, high = None):
    if low is None:
        low = 0
    if high is None:
        high = len (l) - 1
    if high < low:
        return ("Not Found")
    midpoint = (low + high) // 2
    if l[midpoint] == target:
       return midpoint
    elif target < l[midpoint]:
        return binary_search (l, target, low, midpoint - 1)
    else:
        return binary_search (l, target, midpoint + 1, high)

if __name__=='__main__':
    length = 10000
    sorted_list = set()
    while len(sorted_list) < length:
        sorted_list.add(random.randint(-3*length, 3*length))
    sorted_list = sorted(list(sorted_list))
    
    #For Seq_search
    start = time.time()
    for target in sorted_list:
        seq_search(sorted_list, target)
    end = time.time()
    print ("Sequential Serach time was: ", end-start, ' seconds')

    #for binary_search
    start = time.time()
    for target in sorted_list:
        binary_search(sorted_list, target)
    end = time.time()
    print ("Binary Serach time was: ", end-start, ' seconds')