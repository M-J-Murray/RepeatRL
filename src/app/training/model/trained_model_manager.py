from app.training.trainer import Trainer
from app.training.training_stats import TrainingStats


class TrainedModelManager(object):

    def __init__(self, save_dir):
        super(TrainedModelManager).__init__()
        self.save_dir = save_dir
        self.trained_models = []

    def save_trained_model(self, trained_model_id, trainer: Trainer, training_stats: TrainingStats):
        trainer.save(self.save_dir, trained_model_id)
        training_stats.save(self.save_dir, trained_model_id)
        self.trained_models.append(trained_model_id)

    def load_trained_model(self, trained_model_id) -> (Trainer, TrainingStats):
        return Trainer.load(self.save_dir, trained_model_id), TrainingStats.load(self.save_dir, trained_model_id)

    def delete_trained_model(self, trained_model_id):
        Trainer.delete_save(self.save_dir, trained_model_id)
        TrainingStats.delete_save(self.save_dir, trained_model_id)
        del self.trained_models[self.trained_models.index(trained_model_id)]