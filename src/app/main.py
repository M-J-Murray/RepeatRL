from app.gui.repeat_app import RepeatApp
from app.audio.audio_manager import AudioManager
from app.training.training_manager import TrainingManager
from app.training.model.model_manager import ModelManager

if __name__ == '__main__':
    audio_manager = AudioManager("C:\\Users\\michael\\PycharmProjects\\soundDL\\resources\\audio\\", rate=16000, chunk=1600)
    model_manager = ModelManager("C:\\Users\\michael\\PycharmProjects\\soundDL\\resources\\models\\")
    training_manager = TrainingManager("C:\\Users\\michael\\PycharmProjects\\soundDL\\resources\\training\\")
    RepeatApp(audio_manager, model_manager, training_manager).run()
