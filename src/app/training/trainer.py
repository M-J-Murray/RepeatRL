class Trainer(object):

    def __init__(self, encoder, memory, decoder):
        super(Trainer).__init__()
        self.encoder = encoder
        self.memory = memory
        self.decoder = decoder

    def save(self, save_dir, trained_model_id):
        pass

    @staticmethod
    def delete_save(save_dir, trained_model_id):
        pass

    @staticmethod
    def load(save_dir, trained_model_id):
        pass
