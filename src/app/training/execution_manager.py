
class ExecutionManager(object):

    def __init__(self, model_manager, training_manager, trained_model_manager):
        super(ExecutionManager).__init__()

        self.model_manager = model_manager
        self.training_manager = training_manager
        self.trained_model_manager = trained_model_manager

        self.active_models = []

    def start_training(self, training_id):
        if training_id in self.active_models:
            raise Exception("Attempted to request execution of same training definition twice")
        self.active_models.append(training_id)
