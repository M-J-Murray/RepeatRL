from app.training.worker import Worker
from app.audio.audio_manager import AudioManager
from app.training.training_manager import TrainingManager
from app.training.model.model_manager import ModelManager
from app.training.model.trained_model_manager import TrainedModelManager
from app.training.training_stats import TrainingStats
from app.event_listener import EventListener
from threading import Thread
from multiprocessing import Queue


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


class ExecutionManager(Thread):

    def __init__(self, audio_manager: AudioManager, model_manager: ModelManager, training_manager: TrainingManager, trained_model_manager: TrainedModelManager):
        Thread.__init__(self)

        self.audio_manager = audio_manager
        self.model_manager = model_manager
        self.training_manager = training_manager
        self.trained_model_manager = trained_model_manager

        self.active_workers = dict()
        self.active_trainers = dict()
        self.training_stats = dict()

        EventListener.add_listener("worker_finished", self.check_for_finished)

        self.result_queue = Queue()

    def run(self):
        while True:
            trained_model_id, accuracy, is_done = self.result_queue.get()
            self.training_stats[trained_model_id].update(accuracy)
            if is_done:
                self.stop_training(trained_model_id)

    def all_trained_model_ids(self):
        return list(self.active_workers.keys()) + self.trained_model_manager.trained_models

    def generate_next_id(self, training_id, model_id):
        proposed_id = training_id + "-" + model_id + "-"
        greatest = 0
        for training_id in self.all_trained_model_ids():
            if training_id[:len(proposed_id)] == proposed_id and is_int(training_id[len(proposed_id):len(training_id)]):
                value = int(training_id[len(proposed_id):len(training_id)])
                if value > greatest:
                    greatest = value

        return proposed_id + "V" + str(greatest + 1)

    def start_training(self, training_id):
        if training_id in self.active_workers:
            raise Exception("Attempted to request execution of same training definition twice")
        training_definition = self.training_manager.load_training(training_id)
        trained_model_id = self.generate_next_id(training_id, training_definition.model_id)
        model_definition = self.model_manager.load_model(training_definition.model_id)
        trainer = model_definition.generate_trainer()
        self.active_trainers[trained_model_id] = trainer
        training_stats = TrainingStats(self.audio_manager.all_audio_ids())
        self.training_stats[trained_model_id] = training_stats
        worker = Worker(trained_model_id, self.audio_manager, training_definition, trainer, self.result_queue)
        worker.start()
        self.active_workers[trained_model_id] = worker
        EventListener.trigger_event("update_trained_models")

    def check_for_finished(self):
        for trained_model_id in self.active_workers:
            if self.active_workers[trained_model_id].is_finished():
                self.stop_training(trained_model_id)

    def stop_training(self, trained_model_id):
        self.active_workers[trained_model_id].finished = True
        self.active_workers[trained_model_id].join()
        self.trained_model_manager.save_trained_model(trained_model_id, self.active_trainers[trained_model_id], self.training_stats[trained_model_id])
        del self.active_workers[trained_model_id]
        del self.active_trainers[trained_model_id]
        del self.training_stats[trained_model_id]
        EventListener.trigger_event("update_trained_models")
