from enum import Enum
import json


# class FinishCriteria(Enum):
#     ITERATIONS = 1,
#     ACCURACY = 2,
#     TIME = 3


def from_json(json_data):
    data_dict = json.loads(json_data)
    definition = TrainingDefinition()
    definition.model_id = data_dict["model_id"]
    definition.learning_rate = data_dict["learning_rate"]
    definition.test_split = data_dict["test_split"]
    definition.iterations = data_dict["iterations"]
    return definition


class TrainingDefinition(object):

    def __init__(self):
        super(TrainingDefinition).__init__()
        self.model_id = None
        self.learning_rate = 0.001
        self.test_split = 0.1
        self.iterations = 1000

    def to_json(self):
        return json.dumps({
            "model_id": self.model_id,
            "learning_rate": self.learning_rate,
            "test_split": self.test_split,
            "iterations": self.iterations
        })
