from collections import OrderedDict
import os
from app.training.model.model_definition import ModelDefinition


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


class ModelManager(object):

    def __init__(self, save_dir):
        super(ModelManager).__init__()
        self.save_dir = save_dir
        self.unsaved_models = OrderedDict()
        self.model_files = []

    def all_model_ids(self):
        return list(self.unsaved_models) + self.model_files

    def generate_model_id(self):
        greatest = 0
        for model_id in self.all_model_ids():
            if model_id[:6] == "Model " and is_int(model_id[6:len(model_id)]):
                value = int(model_id[6:len(model_id)])
                if value > greatest:
                    greatest = value

        return "Model " + str(greatest + 1)

    def new_model(self):
        model_id = self.generate_model_id()
        self.unsaved_models[model_id] = ModelDefinition()
        return model_id

    def save_model(self, model_id):
        pass

    def delete_model(self, model_id):
        if model_id in self.unsaved_models:
            del self.unsaved_models[model_id]
        else:
            os.remove(self.save_dir + "/" + model_id + ".json")
            del self.model_files[self.model_files.index(model_id)]

    def rename_model(self, audio_id, new_id):
        if audio_id in self.unsaved_models:
            if new_id in self.all_model_ids():
                raise Exception("New audio name is already taken")
            else:
                self.unsaved_models[new_id] = self.unsaved_models[audio_id]
                del self.unsaved_models[audio_id]
        else:
            if new_id in self.all_model_ids():
                raise Exception("New audio name is already taken")
            else:
                os.rename(self.save_dir + "/" + audio_id + ".json",
                          self.save_dir + "/" + new_id + ".json")
                self.model_files[self.model_files.index(audio_id)] = new_id
