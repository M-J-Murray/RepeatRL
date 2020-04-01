from app.training.model.model_definition import ModelDefinition


class TrainingResult(object):

    def __init__(self):
        super(TrainingResult).__init__()
        self.model_definition = None
        self.audio_files = None
        self.model_parameters = None
