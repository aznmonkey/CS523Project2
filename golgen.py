import numpy as np
import copy

def multirun(runs, iterations, size, proportion):
    while runs > 0:
        initial = init(size, proportion)
        file=open('output'+str(runs)+'.txt','w')
        file.write(",".join([str(n) for n in flatten(initial).tolist()])+"\n")
        for i in range(iterations):
            initial = definerules(initial)
            file.write(",".join([str(n) for n in flatten(initial).tolist()])+"\n")
        file.close()
        runs -= 1

def init(size, proportion):
    init_array = np.random.rand(size,size)
    for i in range(size):
        for j in range(size):
            if init_array[i][j] < proportion:
                init_array[i][j] = 1
            else: 
                init_array[i][j] = 0
    init_array = init_array.astype(int)
    return init_array

def definerules(init_array):
    modified_array = copy.deepcopy(init_array)
    length = len(init_array)
    for i in range(length):
        width = len(init_array[i])
        for j in range(width):
            alive = 0

            if i > 0:
                if j > 0 and init_array[i-1][j-1] == 1:
                    alive += 1
                if j < width-1 and init_array[i-1][j+1] == 1:
                    alive += 1
                if init_array[i-1][j] == 1:
                    alive += 1

            if i < length - 1:
                if j > 0 and init_array[i+1][j-1] == 1:
                    alive += 1
                if j < width-1 and init_array[i+1][j+1] == 1:
                    alive += 1
                if init_array[i+1][j] == 1:
                    alive += 1

            if j > 0 and init_array[i][j-1] == 1:
                alive += 1

            if j < width-1 and init_array[i][j+1] == 1:
                alive += 1


            if init_array[i][j] == 1:
                if alive == 2 or alive == 3:
                    modified_array[i][j] = 1
                else:
                    modified_array[i][j] = 0
            else:
                if alive == 3:
                    modified_array[i][j] = 1
                else:
                    modified_array[i][j] = 0
    
    return modified_array
            

def flatten(m_array):
    m_array = np.reshape(m_array, len(m_array)*len(m_array[0]))
    return m_array

if __name__ == '__main__':
    multirun(10, 30, 100, .02)