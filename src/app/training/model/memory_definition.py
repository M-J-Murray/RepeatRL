from app.training.model.memory_model import MemoryModel
import json


def from_json(json_data):
    data_dict = json.loads(json_data)
    definition = MemoryDefinition()
    definition.hidden_n = data_dict["hidden_n"]
    definition.loop_n = data_dict["loop_n"]
    definition.tail_arch = data_dict["tail_arch"]
    return definition


class MemoryDefinition(object):

    def __init__(self):
        super(MemoryDefinition).__init__()
        self.hidden_n = 1
        self.loop_n = 1
        self.tail_arch = [1, 1]

    def generate_model(self):
        return MemoryModel(self.hidden_n, self.loop_n, self.tail_arch)

    def to_json(self):
        return json.dumps({
            "hidden_n": self.hidden_n,
            "loop_n": self.loop_n,
            "tail_arch": self.tail_arch
        })