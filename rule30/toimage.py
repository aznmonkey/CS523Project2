import scipy.misc
import numpy as np
from skimage.draw import line_aa

'''
reads file and returns raw data
'''
def read_file(fname):
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content
'''
convert data to image array
flag == 1 for training data
flag == 0 for predicted data
'''
def to_image(data, flag):
    if flag == 1:
        for i in range(len(data[0])/2):
            if i == 0:
                image = np.array([int(float(x))*256 for x in data[i].split(',')])
        ##        print(image)
            else:
                temp_list = np.array([int(float(x))*256 for x in data[i].split(',')])
                image = np.vstack((image, temp_list))
    else:
        for i in range(len(data[0])/4):
            if i == 0:
                image = np.array([int(float(x))*256 for x in data[i].split(',')])
        ##        print(image)
            else:
                temp_list = np.array([int(float(x))*256 for x in data[i].split(',')])
                image = np.vstack((image, temp_list))
    return image



if __name__ == '__main__':
    original = to_image(read_file('output1.txt'), 1)
    predicted = to_image(read_file('predicted.txt'), 0)
    scipy.misc.imsave("original.png", original)
    scipy.misc.imsave("predicted2.png", predicted)

