import numpy as np
import copy

def init():
    init_array = np.random.randint(2, size=(20,20))
    ##print(init_array)
    return init_array

def definerules(init_array):
    modified_array = copy.deepcopy(init_array)
    length = len(init_array)
    width = len(init_array[0])
    for i in range(length):
        for j in range(width):
            alive = 0

            if i > 0 and j > 0:
                if init_array[i-1][j-1] == 1:
                    alive += 1

            if i > 0:
                if init_array[i-1][j] == 1:
                    alive += 1

            if i > 0 and j < width-1:
                if init_array[i-1][j+1] == 1:
                    alive += 1

            if j > 0:
                if init_array[i][j-1] == 1:
                    alive += 1

            if j < width-1:
                if init_array[i][j+1] == 1:
                    alive += 1

            if i < length-1 and j > 0:
                if init_array[i+1][j-1] == 1:
                    alive += 1

            if i < length-1:
                if init_array[i+1][j] == 1:
                    alive += 1

            if i < length-1 and j < width-1:
                if init_array[i+1][j+1] == 1:
                    alive += 1

            if alive == 2 or alive == 3 and init_array[i][j] == 1:
                modified_array[i][j] = 1
            else: modified_array[i][j] = 0

            if init_array[i][j] == 0 and alive == 3:
                modified_array[i][j] = 1
            else: modified_array[i][j] = 0
    
    return modified_array
            

def flatten(m_array):
    m_array = np.reshape(m_array, len(m_array)*len(m_array[0]))
    return m_array

if __name__ == '__main__':
    initial = init()
    file=open('output.txt','w')
    file.write(",".join([str(n) for n in flatten(initial).tolist()])+"\n")    
    for i in range(10):
        initial = definerules(initial)
        file.write(",".join([str(n) for n in flatten(initial).tolist()])+"\n")
    file.close()