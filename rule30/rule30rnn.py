import tensorflow as tf
from tensorflow.nn.rnn_cell import GRUCell, DropoutWrapper, MultiRNNCell


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
        if i%2 == 0:
            sequence.append(content[i])
        else:
            label_sequence.append(content[i])
    return sequence, label_sequence

def unpack_sequence(tensor):
    """Split the single tensor of a sequence into a list of frames."""
    return tf.unpack(tf.transpose(tensor, perm=[1, 0, 2]))

def pack_sequence(sequence):
    """Combine a list of the frames into a single tensor of the sequence."""
    return tf.transpose(tf.pack(sequence), perm=[1, 0, 2])

'''
generate tf example from sequence
'''
def train(sequence, labels):
    num_neurons = 200
    num_layers = 3
    dropout = tf.placeholder(tf.float32)

    cell = GRUCell(num_neurons)  # Or LSTMCell(num_neurons)
    cell = DropoutWrapper(cell, output_keep_prob=dropout)
    cell = MultiRNNCell([cell] * num_layers)

    max_length = len(sequence)

    # Batch size x time steps x features.
    data = tf.placeholder(tf.float32, [None, max_length, len(sequence[0])])
    output, state = tf.nn.dynamic_rnn(cell, data, dtype=tf.float32)

    output = pack_sequence(outputs)

    
if __name__ == '__main__':
    content = read_file('output1.txt')
    ##print(len(content))
    sequence, label_sequence = generate_data(content)
    train(sequence, label_sequence)

