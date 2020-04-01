class Trainer(object):

    def __init__(self, encoder, memory, decoder):
        super(Trainer).__init__()
        self.encoder = encoder
        self.memory = memory
        self.decoder = decoder
