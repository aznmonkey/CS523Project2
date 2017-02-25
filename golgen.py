import numpy as np
import copy

def init():

    init_array = np.random.randint(2, size=(20,20))
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
    initial = init()
    file=open('output.txt','w')
    file.write(",".join([str(n) for n in flatten(initial).tolist()])+"\n")    

    print(",".join([str(n) for n in flatten(initial).tolist()])+"\n")

    for i in range(10):
        print("step" + str(i))
        initial = definerules(initial)
        for m in range(len(initial)):
            print(",".join([str(initial[m][n]) for n in range(len(initial[m]))]))
        print("\n")

        file.write(",".join([str(n) for n in flatten(initial).tolist()])+"\n")
    file.close()