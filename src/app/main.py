from app.gui.repeat_app import RepeatApp
from app.audio.audio_manager import AudioManager
from app.training.model.model_manager import ModelManager
from app.training.training_manager import TrainingManager
from app.training.execution_manager import ExecutionManager
from app.training.model.trained_model_manager import TrainedModelManager


if __name__ == '__main__':
    audio_manager = AudioManager("C:\\Users\\michael\\PycharmProjects\\soundDL\\resources\\audio\\", rate=16000, chunk=1600)
    model_manager = ModelManager("C:\\Users\\michael\\PycharmProjects\\soundDL\\resources\\models\\")
    training_manager = TrainingManager("C:\\Users\\michael\\PycharmProjects\\soundDL\\resources\\training\\")
    trained_model_manager = TrainedModelManager("C:\\Users\\michael\\PycharmProjects\\soundDL\\resources\\trained\\")
    execution_manager = ExecutionManager(model_manager, training_manager, trained_model_manager)
    RepeatApp(audio_manager, model_manager, training_manager, trained_model_manager, execution_manager).run()
