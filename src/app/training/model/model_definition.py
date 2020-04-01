from app.training.trainer import Trainer
from app.training.model.translation_definition import TranslationDefinition
from app.training.model.memory_definition import MemoryDefinition


class ModelDefinition(object):

    def __init__(self):
        super(ModelDefinition).__init__()
        self.encoder_definition = None
        self.memory_definition = None
        self.output_definition = None

    def generate_trainer(self):
        return Trainer(
            self.encoder_definition.generate_model(),
            self.memory_definition.generate_model(),
            self.output_definition.generate_model(),
        )