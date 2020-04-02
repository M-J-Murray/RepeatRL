from collections import OrderedDict
import os

from app.training.training_definition import TrainingDefinition
from app.training.training_definition import from_json


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


class TrainingManager(object):

    def __init__(self, save_dir):
        super(TrainingManager).__init__()
        self.save_dir = save_dir
        self.unsaved_training = OrderedDict()
        self.training_files = []
        self.check_for_saved_training()

    def check_for_saved_training(self):
        for f in os.listdir(self.save_dir):
            path = os.path.join(self.save_dir, f)
            if os.path.isfile(path):
                self.training_files.append(f[:-5])

    def all_training_ids(self):
        return sorted(list(self.unsaved_training) + self.training_files)

    def generate_training_id(self):
        greatest = 0
        for training_id in self.all_training_ids():
            if training_id[:9] == "Training " and is_int(training_id[9:len(training_id)]):
                value = int(training_id[9:len(training_id)])
                if value > greatest:
                    greatest = value

        return "Training " + str(greatest + 1)

    def new_training(self):
        training_id = self.generate_training_id()
        self.unsaved_training[training_id] = TrainingDefinition()
        return training_id

    def save_training(self, training_id):
        training_json = self.unsaved_training[training_id].to_json()
        with open(self.save_dir + "/" + training_id + ".json", "w") as file:
            file.write(training_json)
        del self.unsaved_training[training_id]
        self.training_files.append(training_id)

    def load_training(self, training_id):
        if training_id in self.unsaved_training:
            return self.unsaved_training[training_id]

        with open(self.save_dir + "/" + training_id + ".json", "r") as file:
            training_json = file.readline()
        return from_json(training_json)

    def update_training(self, training_id, training_definition):
        if training_id not in self.unsaved_training:
            del self.training_files[self.training_files.index(training_id)]
        self.unsaved_training[training_id] = training_definition

    def delete_training(self, training_id):
        if training_id in self.unsaved_training:
            del self.unsaved_training[training_id]
        else:
            os.remove(self.save_dir + "/" + training_id + ".json")
            del self.training_files[self.training_files.index(training_id)]

    def rename_training(self, training_id, new_id):
        if training_id in self.unsaved_training:
            if new_id in self.all_training_ids():
                raise Exception("New training name is already taken")
            else:
                self.unsaved_training[new_id] = self.unsaved_training[training_id]
                del self.unsaved_training[training_id]
        else:
            if new_id in self.all_training_ids():
                raise Exception("New training name is already taken")
            else:
                os.rename(self.save_dir + "/" + training_id + ".json",
                          self.save_dir + "/" + new_id + ".json")
                self.training_files[self.training_files.index(training_id)] = new_id
