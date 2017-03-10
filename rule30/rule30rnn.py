import tensorflow as tf
import numpy as np
import time
import datetime
import sys

'''
outputs print to console and text log
'''
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

'''
read raw data from file
'''
def read_file(fname):
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    return content

'''
separate raw data into a sequence along with label sequence outputs
'''
def generate_data(content):
    sequence = []
    label_sequence = []
    for i in range(len(content)):
        content[i] = [int(x) for x in content[i].split(',')]
        if i%2 == 0:
            temp_list = []
            for j in content[i]:
                temp_list.append([j])
            sequence.append(np.array(temp_list))
        else:
            label_sequence.append(content[i])
 ##   print(sequence[0])
 ##   print(len(sequence), len(label_sequence))
    return sequence, label_sequence

'''
normalize predicted outputs from nn
'''
def normalize(output):
   normalized_output = output/np.amax(output)
   for i in range(len(normalized_output)):
       normalized_output[i] = np.around(normalized_output[i])
   return normalized_output

'''
turn output format to input format
'''
def output_to_input(normalized_output):
   new_input = []
   temp_list = []
   for j in range(len(normalized_output[0])):
       temp_list.append([int(normalized_output[0][j])])
   new_input.append(np.array(temp_list))
   return new_input

'''
output prediction to file
'''
def generate_predictions(prediction, intial_run):
    if intial_run == 1:
        file1 = open('output2.txt', 'w')
    else:
        file1 = open('output2.txt','a')
    file1.write(",".join([str(n) for n in prediction[0].tolist()])+"\n")

'''
generate tf example from sequence
'''
def train(sequence, labels):
    NUM_EXAMPLES = 100000
    test_input = sequence[NUM_EXAMPLES:]
    test_output = labels[NUM_EXAMPLES:] #everything beyond 1,000
    
    train_input = sequence[:NUM_EXAMPLES]
    train_output = labels[:NUM_EXAMPLES] #till 1,000

    data = tf.placeholder(tf.float32, [None, 30, 1])
    target = tf.placeholder(tf.float32, [None, 30])

    num_hidden = 36
    cell = tf.nn.rnn_cell.LSTMCell(num_hidden,state_is_tuple=True)

    val, state = tf.nn.dynamic_rnn(cell, data, dtype=tf.float32)

    val = tf.transpose(val, [1,0,2])
    last = tf.gather(val, int(val.get_shape()[0]) - 1)
    
    weight = tf.Variable(tf.truncated_normal([num_hidden, int(target.get_shape()[1])]))
    bias = tf.Variable(tf.constant(0.1, shape=[target.get_shape()[1]]))
    print("weight shape: ", weight.get_shape())
    print("bias shape: ", bias.get_shape())
    
    prediction = tf.nn.softmax(tf.matmul(last, weight) + bias)
    print("prediction shape: ", prediction.get_shape())
    print("target shape: ", target.get_shape())
    cross_entropy = -tf.reduce_sum(target * tf.log(tf.clip_by_value(prediction,1e-10,1.0)))

    optimizer = tf.train.AdamOptimizer()
    minimize = optimizer.minimize(cross_entropy)
    print("target argmax", tf.argmax(target,1))
    print("prediction argmax:", tf.argmax(prediction,1))
    mistakes = tf.not_equal(tf.argmax(target, 1), tf.argmax(prediction, 1))
    error = tf.reduce_mean(tf.cast(mistakes, tf.float32))

    init_op = tf.initialize_all_variables()
    sess = tf.Session()
    sess.run(init_op)   

    batch_size = 1000
    no_of_batches = int(len(train_input)/batch_size)
    epoch = 1
    for i in range(epoch):
        ptr = 0
        for j in range(no_of_batches):
            inp, out = train_input[ptr:ptr+batch_size], train_output[ptr:ptr+batch_size]
            ptr+=batch_size
            sess.run(minimize,{data: inp, target: out})
        print ("Epoch - ",str(i))
    incorrect = sess.run(error,{data: test_input, target: test_output})
    print('Epoch {:2d} error {:3.1f}%'.format(i + 1, 100 * incorrect))
    
    predicted_output = sess.run(prediction,{data: [[[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]]]})
    generate_predictions(normalize(predicted_output), 1)
    iterations = 30
    while iterations > 0:
        predicted_output = sess.run(prediction,{data: output_to_input(normalize(predicted_output))})
        generate_predictions(normalize(predicted_output), 0)
        iterations -=1
    sess.close()

if __name__ == '__main__':
    ts = time.time()
    f = open('log-'+str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S'))+'.txt', 'w')
    sys.stdout = Tee(sys.stdout, f)

    content = read_file('output1.txt')
    ##print(len(content))
    sequence, label_sequence = generate_data(content)
    train(sequence, label_sequence)

