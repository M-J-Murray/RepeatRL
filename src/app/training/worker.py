import torch.multiprocessing as mp
from app.audio.audio_manager import AudioManager
from app.training.training_definition import TrainingDefinition
from app.training.trainer import Trainer

from app.event_listener import EventListener

import time


class Worker(mp.Process):

    def __init__(self, trained_model_id, audio_manager: AudioManager, training_definition: TrainingDefinition, trainer: Trainer, result_queue: mp.Queue):
        super(Worker, self).__init__()
        self.trained_model_id = trained_model_id
        self.audio_manager = audio_manager
        self.training_definition = training_definition
        self.trainer = trainer
        self.finished = False
        self.result_queue = result_queue

    def is_finished(self):
        return self.finished

    def run(self):
        try:
            print("Starting Worker")

            for i in range(self.training_definition.iterations):
                time.sleep(0.1)

            self.finished = True
            print("Worker Finished")
            self.result_queue.put((self.trained_model_id, 1, True))
        except Exception as e:
            raise e
