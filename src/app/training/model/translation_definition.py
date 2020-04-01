from app.training.model.translation_model import TranslationModel


class TranslationDefinition(object):

    def __init__(self):
        super(TranslationDefinition).__init__()
        self.lstm_arch = None
        self.tail_arch = None
        self.is_encoder = None

    def generate_model(self):
        return TranslationModel(self.lstm_arch, self.tail_arch, self.is_encoder)
