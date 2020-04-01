from app.training.model.memory_model import MemoryModel


class MemoryDefinition(object):

    def __init__(self):
        super(MemoryDefinition).__init__()
        self.hidden_n = None
        self.loop_n = None
        self.tail_arch = None

    def generate_model(self):
        return MemoryModel(self.hidden_n, self.loop_n, self.tail_arch)
