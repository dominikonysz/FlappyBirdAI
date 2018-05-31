import numpy as np


class NeuralNet:
    counter = 0

    def __init__(self, input_size, hidden_sizes, output_size):
        self.id = NeuralNet.counter
        NeuralNet.counter += 1

        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size

        self.weights = {}
        self.biases = {}

        max_dev = 4

        for h_layer in range(len(hidden_sizes)):
            if h_layer == 0:
                self.weights['h{}'.format(h_layer)] = np.random.rand(input_size, hidden_sizes[h_layer]) * max_dev - max_dev/2
                self.biases['h{}'.format(h_layer)] = np.random.rand(hidden_sizes[h_layer]) * max_dev - max_dev/2
            else:
                self.weights['h{}'.format(h_layer)] = np.random.rand(hidden_sizes[h_layer - 1], hidden_sizes[h_layer]) * max_dev - max_dev/2
                self.biases['h{}'.format(h_layer)] = np.random.rand(hidden_sizes[h_layer]) * max_dev - max_dev/2

        if len(hidden_sizes) > 0:
            self.weights['o'] = np.random.rand(hidden_sizes[-1], output_size) * max_dev - max_dev/2
            self.biases['o'] = np.random.rand(output_size) * max_dev - max_dev/2
        else:
            self.weights['o'] = np.random.rand(input_size, output_size) * max_dev - max_dev/2
            self.biases['o'] = np.random.rand(output_size) * max_dev - max_dev/2

    def predict(self, data):
        out = self.compute(data)
        return out

    def compute(self, x):
        out = x
        # hidden layers
        for h_layer in range(len(self.weights) - 1):
            out = np.add(np.dot(out, self.weights['h{}'.format(h_layer)]), self.biases['h{}'.format(h_layer)])
            out = np.maximum(0, out, out)

        # output layer
        out = np.add(np.matmul(out, self.weights['o']), self.biases['o'])
        out = 2 / (1 + np.exp(-out)) - 1
        return out

    def mutate(self):
        self.adjust_weights()

    def adjust_weights(self):
        for key in self.weights.keys():
            shape = self.weights[key].shape
            max_diff = 0.8
            self.weights[key] = self.weights[key] + (np.random.rand(shape[0], shape[1]) * max_diff - max_diff/2)
            self.biases[key] = self.biases[key] + (np.random.rand(shape[1]) * max_diff - max_diff/2)

    def copy(self):
        new_nn = NeuralNet(self.input_size, self.hidden_sizes, self.output_size)
        for key in self.weights.keys():
            new_nn.weights[key] = self.weights[key]
            new_nn.biases[key] = self.biases[key]
        return new_nn
