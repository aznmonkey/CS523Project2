# rule30 RNN Generator

#Requirements:
Python 2.7.12 (3.5 should also work but is tested)
tensorflow
numpy
scipy
scikit-image (to generate the pngs)

#How to run:
The RNN is located in the rule30rnn directory
To generate the training set run rule30gen.py, by default it generates 2000 sets of rule30 games of width 30 and 100 iterations

To train the network and generate predictions run rule30rnn.py, the INITIAL_SEED is the first prediction that is fed into the trained RNN. It will generate a output file with the predicted outputs (output2.txt by default).

To generate pngs run toimage.py to generate images of the outputs (outputs to predicted2.png and original.png for the predicted and original data respectively)

#How it works:
Rule 30 is a simple deterministic cellular automata:
https://en.wikipedia.org/wiki/Rule_30
The RNN is a simple RNN with 1 hidden layer 
The every other row of the training data is used as the input and the rest of the rows are used as the output to be used to generate the error.

#Samples
Below is an image of part of the original training set:
![Alt text](/rule30/original-zoom.png?raw=true "Original")
Predicted output using RNN trained with Epoch 1:
![Alt text](/rule30/epoch1-zoom.png?raw=true "Original")
Epoch 1000:
![Alt text](/rule30/predicted-zoom.png?raw=true "Original")