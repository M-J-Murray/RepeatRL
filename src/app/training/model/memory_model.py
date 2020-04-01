import torch.nn as nn
import torch.nn


class MemoryModel(nn.Module):

    def __init__(self, hidden_n, loop_n, tail_arch):
        super(MemoryModel, self).__init__()
        self.encoder = nn.LSTM(hidden_n, hidden_n)
        self.decoder = nn.LSTM(hidden_n, hidden_n)
        self.state_shape = (1, 1, hidden_n)
        self.encoded_memory = None
        self.loop_layers = [
            nn.Linear(hidden_n, loop_n),
            nn.Linear(loop_n, hidden_n)
        ]
        self.tail_layers = []
        for i in range(len(tail_arch) - 1):
            self.tail_layers.append(nn.Linear(tail_arch[i], tail_arch[i + 1]))

    def reset_state(self):
        self.encoded_memory = (torch.zeros(*self.state_shape, dtype=torch.float32), torch.zeros(*self.state_shape, dtype=torch.float32))

    def store_memory(self, x):
        self.encoder(x, self.encoded_memory)

    def extract_memory(self):
        self.decoder(self.lstm_state[1], self.encoded_memory)

    def forward(self):
        out = self.lstm_state[0]
        for layer in self.tail_layers:
            out = layer(out)
        return out
