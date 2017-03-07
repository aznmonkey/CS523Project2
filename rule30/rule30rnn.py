import tensorflow as tf
import numpy as np

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
                temp_list.append([content[i][j]])
            sequence.append(np.array(temp_list))
        else:
            label_sequence.append(content[i])
    print(sequence)
    return sequence, label_sequence

'''
generate tf example from sequence
'''
def train(sequence, labels):
    NUM_EXAMPLES = 1000
    test_input = sequence[NUM_EXAMPLES:]
    test_output = labels[NUM_EXAMPLES:] #everything beyond 1,000
    
    train_input = sequence[:NUM_EXAMPLES]
    train_output = labels[:NUM_EXAMPLES] #till 1,000

    data = tf.placeholder(tf.float32, [None, 30, 1])
    target = tf.placeholder(tf.float32, [None, 30])

    num_hidden = 24
    cell = tf.nn.rnn_cell.LSTMCell(num_hidden,state_is_tuple=True)

    val, state = tf.nn.dynamic_rnn(cell, data, dtype=tf.float32)

    val = tf.transpose(val, [1,0,2])
    last = tf.gather(val, int(val.get_shape()[0]) - 1)
    
    weight = tf.Variable(tf.truncated_normal([num_hidden, int(target.get_shape()[1])]))
    bias = tf.Variable(tf.constant(0.1, shape=[target.get_shape()[1]]))

    prediction = tf.nn.softmax(tf.matmul(last, weight) + bias)

    cross_entropy = -tf.reduce_sum(target * tf.log(tf.clip_by_value(prediction,1e-10,1.0)))

    optimizer = tf.train.AdamOptimizer()
    minimize = optimizer.minimize(cross_entropy)

    mistakes = tf.not_equal(tf.argmax(target, 1), tf.argmax(prediction, 1))
    error = tf.reduce_mean(tf.cast(mistakes, tf.float32))

    init_op = tf.initialize_all_variables()
    sess = tf.Session()
    sess.run(init_op)   

    batch_size = 1000
    no_of_batches = int(len(train_input)/batch_size)
    epoch = 1000
    for i in range(epoch):
        ptr = 0
        for j in range(no_of_batches):
            inp, out = train_input[ptr:ptr+batch_size], train_output[ptr:ptr+batch_size]
            ptr+=batch_size
            sess.run(minimize,{data: inp, target: out})
        print ("Epoch - ",str(i))
    incorrect = sess.run(error,{data: test_input, target: test_output})
    print('Epoch {:2d} error {:3.1f}%'.format(i + 1, 100 * incorrect))
    sess.close()

if __name__ == '__main__':
    content = read_file('output1.txt')
    ##print(len(content))
    sequence, label_sequence = generate_data(content)
    train(sequence, label_sequence)

