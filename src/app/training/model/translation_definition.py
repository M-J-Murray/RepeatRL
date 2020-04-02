from app.training.model.translation_model import TranslationModel
import json


def from_json(json_data):
    data_dict = json.loads(json_data)
    definition = TranslationDefinition(is_encoder=data_dict["is_encoder"])
    definition.lstm_arch = data_dict["lstm_arch"]
    definition.tail_arch = data_dict["tail_arch"]
    return definition


class TranslationDefinition(object):

    def __init__(self, is_encoder):
        super(TranslationDefinition).__init__()
        self.lstm_arch = [1, 1]
        self.tail_arch = [1, 1]
        self.is_encoder = is_encoder

    def generate_model(self):
        return TranslationModel(self.lstm_arch, self.tail_arch, self.is_encoder)

    def to_json(self):
        return json.dumps({
            "lstm_arch": self.lstm_arch,
            "tail_arch": self.tail_arch,
            "is_encoder": self.is_encoder
        })
