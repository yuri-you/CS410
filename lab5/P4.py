import argparse

import matplotlib.pyplot as plt
import numpy as np

from utils import (
    calculate_acc,
    data_iterator,
    onehot_encoding,
    plot_decision_boundary,
    prepare_data_moons
)


class Layer(object):
    def __init__(self, name, trainable=False):
        self.name = name
        self.trainable = trainable
        self._saved_tensor = None

    def forward(self, input):
        pass

    def backward(self, grad_output):
        """Take gradients w.r.t the output of this layer and then
        output the gradients w.r.t. to the input of this layer.

        For trainable layer, you may need to record some variables in order to update the parameters when calling update().
        """
        pass

    def update(self, config):
        """Update parameters with information recorded in the last backward."""
        pass

    def _saved_for_backward(self, tensor):
        """The intermediate results computed during forward stage
        can be saved and reused for backward, for saving computation."""
        self._saved_tensor = tensor


class Relu(Layer):
    def __init__(self, name):
        super(Relu, self).__init__(name)

    def forward(self, input):
        self._saved_for_backward(input)
        input[input <= 0] = 0

        return input

    def backward(self, grad_output):
        grad_output[self._saved_tensor<=0]=0
        """Your code here"""

        return grad_output


class Linear(Layer):
    def __init__(self, name, in_num, out_num, init_std):
        super(Linear, self).__init__(name, trainable=True)

        self.in_num = in_num
        self.out_num = out_num
        self.W = np.random.randn(in_num, out_num) * init_std
        self.b = np.zeros(out_num)

        self.grad_W = np.zeros((in_num, out_num))
        self.grad_b = np.zeros(out_num)

        self.diff_W = np.zeros((in_num, out_num))
        self.diff_b = np.zeros(out_num)

    def forward(self, input):
        self._saved_for_backward(input)

        return input.dot(self.W) + self.b

    def backward(self, grad_output):
        """Your code here"""
        self.grad_W=self._saved_tensor.T.dot(grad_output)/len(grad_output)
        self.grad_b=grad_output.mean(axis=0)
        new_grad=grad_output.dot(self.W.T)
        self.W=self.W-self.mm*self.grad_W
        self.b=self.b-self.mm*self.grad_b
        return new_grad

    def update(self, config):
        mm = config['momentum']
        lr = config['learning_rate']
        self.mm=mm
        self.lr=lr
        """Your code here"""

class Network(object):
    def __init__(self):
        self.layer_list = []
        self.params = []
        self.num_layers = 0

    def add(self, layer):
        self.layer_list.append(layer)
        self.num_layers += 1

    def forward(self, input):
        output = input
        for i in range(self.num_layers):
            output = self.layer_list[i].forward(output)

        return output

    def backward(self, grad_output):
        
        """Your code here"""
        new_grad=grad_output
        for i in range(self.num_layers):
            new_grad=self.layer_list[self.num_layers-1-i].backward(new_grad)
        return None

    def update(self, config):
        for i in range(self.num_layers):
            if self.layer_list[i].trainable:
                self.layer_list[i].update(config)

    def predict(self, input):
        y_pred = self.forward(input).argmax(axis=-1)

        return y_pred

class EuclideanLoss:
    def __init__(self, name):
        self.name = name

    def forward(self, input, target):
        return ((target - input) ** 2).mean(axis=0).sum() / 2.

    def backward(self, input, target):
        """Your code here"""
        return (input-target)
        # return None

def train_net(model, loss, config, inputs, labels, batch_size, disp_freq):
    loss_list = []
    acc_list = []
    loss_ = []
    acc_ = []

    for iter_idx, (input, label) in enumerate(data_iterator(inputs, labels, batch_size)):
        target = onehot_encoding(label, 2)

        # Forward.
        output = model.forward(input)

        # Calculate loss.
        loss_value = loss.forward(output, target)

        # Update layers' weights.
        model.update(config)

        # Generate gradient w.r.t loss.
        grad = loss.backward(output, target)

        # Backward.
        model.backward(grad)


        acc_value = calculate_acc(output, label)
        loss_list.append(loss_value)
        acc_list.append(acc_value)

        if iter_idx % disp_freq == 0:
            msg = '  Training iter %d, batch loss %.6f, batch acc %.6f' % (iter_idx, np.mean(loss_list), np.mean(acc_list))
            loss_.append(np.mean(loss_list))
            acc_.append(np.mean(acc_list))
            loss_list = []
            acc_list = []
            print(msg)

    return loss_, acc_

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hidden_dim", type=int, default=20)
    args = parser.parse_args()

    # Prepare data.
    x, y = prepare_data_moons()
    # plot_decision_boundary(x, y)
    # plt.show()

    # Build network.
    model = Network()
    model.add(Linear('fc1', 2, args.hidden_dim, init_std=0.001))
    model.add(Relu('rl1'))
    model.add(Linear('fc2', args.hidden_dim, 2, init_std=0.001))
    model.add(Relu('rl2'))
    loss = EuclideanLoss("loss")
    config = {
        'learning_rate': 1e-3,
        'momentum': 0.9,
        'batch_size': 500,
        'max_epoch': 1000,
        'disp_freq': 50,
        'test_epoch': 5
    }

    # Train.
    for epoch_idx in range(config['max_epoch']):
        print('Training @ %d epoch...' % (epoch_idx))
        a, b = train_net(model, loss, config, x, y, config['batch_size'], config['disp_freq'])

    # Visualize.
    plot_decision_boundary(x, y, lambda x: model.predict(x) == 1)
    plt.show()

if __name__ == "__main__":
    main()
