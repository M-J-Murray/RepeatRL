import json
import os


class TrainingStats(object):
    def __init__(self, audio_ids):
        self.audio_ids = audio_ids
        self.results = []
        self.best = 0
        self.running = 0

    def update(self, accuracy):
        self.results.append(accuracy)
        if len(self.results) == 1:
            self.best = accuracy
        elif accuracy > self.best:
            self.best = accuracy
        self.running = accuracy if len(self.results) == 1 else self.running * 0.99 + accuracy * 0.01

    @staticmethod
    def generate_file_path(save_dir, trained_model_id):
        return save_dir+"/"+trained_model_id+"-stats.json"

    def save(self, save_dir, trained_model_id):
        as_json = json.dumps({
            "audio_ids": self.audio_ids,
            "results": self.results,
            "best": self.best,
            "running": self.running
        })
        with open(TrainingStats.generate_file_path(save_dir, trained_model_id), "w") as file:
            file.write(as_json)

    @staticmethod
    def delete_save(save_dir, trained_model_id):
        os.remove(TrainingStats.generate_file_path(save_dir, trained_model_id))

    @staticmethod
    def load(save_dir, trained_model_id):
        with open(TrainingStats.generate_file_path(save_dir, trained_model_id), "r") as file:
            json_data = json.loads(file.readline())
        stats = TrainingStats(json_data["audio_ids"])
        stats.results = json_data["results"]
        stats.best = json_data["best"]
        stats.running = json_data["running"]
        return stats
