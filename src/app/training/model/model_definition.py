from app.training.trainer import Trainer
from app.training.model.translation_definition import TranslationDefinition
from app.training.model.translation_definition import from_json as trans_from_json
from app.training.model.memory_definition import MemoryDefinition
from app.training.model.memory_definition import from_json as mem_from_json
import json


def from_json(json_data):
    data_dict = json.loads(json_data)
    definition = ModelDefinition()
    definition.encoder_definition = trans_from_json(data_dict["encoder_definition"])
    definition.memory_definition = mem_from_json(data_dict["memory_definition"])
    definition.decoder_definition = trans_from_json(data_dict["decoder_definition"])
    return definition


class ModelDefinition(object):

    def __init__(self):
        super(ModelDefinition).__init__()
        self.encoder_definition = TranslationDefinition(is_encoder=True)
        self.memory_definition = MemoryDefinition()
        self.decoder_definition = TranslationDefinition(is_encoder=False)

    def generate_trainer(self):
        return Trainer(
            self.encoder_definition.generate_model(),
            self.memory_definition.generate_model(),
            self.decoder_definition.generate_model(),
        )

    def to_json(self):
        return json.dumps({
            "encoder_definition": self.encoder_definition.to_json(),
            "memory_definition": self.memory_definition.to_json(),
            "decoder_definition": self.decoder_definition.to_json()
        })
