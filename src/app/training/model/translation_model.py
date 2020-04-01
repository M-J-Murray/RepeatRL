import torch.nn as nn
import torch.nn
from torch.nn.functional import relu, tanh


class TranslationModel(nn.Module):

    def __init__(self, lstm_arch, tail_arch, is_encoder):
        super(TranslationModel, self).__init__()
        self.lstm_arch = lstm_arch
        self.tail_arch = tail_arch
        self.lstm_layers = []
        self.state_shapes = []
        self.lstm_states = []
        self.lstm_out_shape = lstm_arch[len(lstm_arch)-1]
        self.tail_layers = []
        for i in range(len(lstm_arch) - 1):
            self.lstm_layers.append(nn.LSTM(lstm_arch[i], lstm_arch[i + 1]))
            self.state_shapes.append((1, 1, lstm_arch[i + 1]))
        for i in range(len(tail_arch) - 1):
            self.tail_layers.append(nn.Linear(tail_arch[i], tail_arch[i + 1]))
        self.is_encoder = is_encoder

    def reset_state(self):
        self.lstm_states = []
        for state_shape in self.state_shapes:
            self.lstm_states.append(
                (torch.zeros(*state_shape, dtype=torch.float32), torch.zeros(*state_shape, dtype=torch.float32)))

    def forward(self, x):
        outs = [x]

        for i in range(len(self.lstm_layers)):
            out, new_state = self.lstm_layers[i](outs[len(outs) - 1], self.layer_states[i])
            outs.append(relu(self.out))
            self.layer_states[i] = new_state

        outs.append(self.tail_layers[0](outs[len(outs) - 1]).view(1, 1, self.lstm_out_shape))
        for i in range(1, len(self.tail_layers)):
            if i == len(self.tail_layers)-1 and not self.is_encoder:
                outs.append(tanh(self.tail_layers[i](outs[len(outs) - 1])))
            else:
                outs.append(relu(self.tail_layers[i](outs[len(outs) - 1])))

        return outs
