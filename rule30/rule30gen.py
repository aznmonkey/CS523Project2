import numpy as np
import copy

def multirun(runs, size):
    while runs > 0:
        initial = init(size)
        file = open('output'+str(runs)+'.txt', 'w')
        file.write(",".join([str(n) for n in initial.tolist()])+"\n")
        for i in range(int(size/2)):
            initial = definerules(initial)
            file.write(",".join([str(n) for n in initial.tolist()])+"\n")
        file.close()
        runs -= 1

def init(size):
    init_array = np.zeros((size,), dtype=np.int)
    init_array[int(len(init_array)/2)] = 1
    ##print(init_array)
    return init_array

def definerules(init_array):
    modified_array = copy.deepcopy(init_array)
    length = len(init_array)
    for i in range(length):
        if i > 0 and i < length-1:
            if init_array[i+1] == 1 and init_array[i-1] == 1 and init_array[i] == 1:
                modified_array[i] = 0
            elif init_array[i-1] == 1 and init_array[i] == 1:
                modified_array[i] = 0
            elif init_array[i+1] == 1 and init_array[i-1] == 1:
                modified_array[i] = 0
            elif init_array[i-1] == 1:
                modified_array[i] = 1
            elif init_array[i+1] == 1 and init_array[i] == 1:
                modified_array[i] = 1
            elif init_array[i] == 1:
                modified_array[i] = 1
            elif init_array[i+1] == 1:
                modified_array[i] = 1
            else:
                modified_array[i] = 0

        if i == 0:
            if init_array[i+1] == 1 and init_array[i] == 1:
                modified_array[i] = 1
            elif init_array[i] == 1:
                modified_array[i] = 1
            elif init_array[i+1] == 1:
                modified_array[i] = 1
            else:
                modified_array[i] = 0

        if i == length-1:
            if init_array[i-1] == 1 and init_array[i] == 1:
                modified_array[i] = 0
            elif init_array[i-1] == 1:
                modified_array[i] = 1
            elif init_array[i] == 1:
                modified_array[i] = 1
            else:
                modified_array[i] = 0

    return modified_array
            
if __name__ == '__main__':
    multirun(100, 100)