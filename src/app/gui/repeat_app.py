from kivy.app import App
from app.gui.util.sparse_grid_layout import SparseGridLayout
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.core.window import Window
from kivy.uix.popup import Popup

from app.gui.audio_view.audio_view import AudioView
from app.gui.model_view.model_view import ModelView
from app.gui.training_view.training_view import TrainingView
from app.gui.trained_model_view.trained_model_view import TrainedModelView

from kivy.uix.label import Label


class RepeatException(ExceptionHandler):

    def handle_exception(self, exception):
        app = RepeatApp.get_running_app()
        app.error_label.text = str(exception)
        app.error_popup.open()
        return ExceptionManager.PASS


# ExceptionManager.add_handler(RepeatException())


class RepeatApp(App):

    def __init__(self, audio_manager, model_manager, training_manager, trained_model_manager, execution_manager, **kwargs):
        self.audio_manager = audio_manager
        self.model_manager = model_manager
        self.training_manager = training_manager
        self.trained_model_manager = trained_model_manager
        self.execution_manager = execution_manager

        self.error_label = Label(text="")
        self.error_popup = Popup(title="Error", content=self.error_label, auto_dismiss=True, pos_hint={"x": 0.2, "y": 0.4}, size_hint=(0.6, 0.2))

        super().__init__(**kwargs)

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1600, 600)
        Window.left = 200
        Window.top = 200

        layout = SparseGridLayout(rows=1, cols=4)
        layout.add_entry(AudioView(self.audio_manager), position=(0, 0), shape=(1, 1))
        training_view = TrainingView(self.audio_manager, self.model_manager, self.training_manager, self.execution_manager)
        layout.add_entry(training_view, position=(0, 2), shape=(1, 1))
        layout.add_entry(ModelView(self.model_manager, training_view.training_editor.update_model_entries), position=(0, 1), shape=(1, 1))
        layout.add_entry(TrainedModelView(self.audio_manager, self.model_manager, self.training_manager, self.trained_model_manager), position=(0, 3), shape=(1, 1))

        return layout
