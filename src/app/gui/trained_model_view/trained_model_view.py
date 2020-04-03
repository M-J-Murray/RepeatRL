from app.gui.util.sparse_grid_layout import SparseGridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from kivy.uix.label import Label
from kivy.uix.button import Button

from app.audio.audio_manager import AudioManager
from app.training.execution_manager import ExecutionManager
from app.training.model.trained_model_manager import TrainedModelManager
from app.gui.trained_model_view.trained_model_entry import TrainedModelEntry
from app.gui.trained_model_view.training_result_view import TrainingResultView
from app.event_listener import EventListener


class TrainedModelView(SparseGridLayout):

    def __init__(self, audio_manager: AudioManager, execution_manager: ExecutionManager, trained_model_manager: TrainedModelManager):
        self.audio_manager = audio_manager
        self.execution_manager = execution_manager
        self.trained_model_manager = trained_model_manager
        super().__init__(rows=20, cols=1)
        self.add_entry(Label(text='Trained Models', font_size='20sp', color=[0, 0, 0, 1]), position=(18, 0), shape=(2, 1))

        self.trained_models_scroll = ScrollView()
        self.add_entry(self.trained_models_scroll, position=(11, 0), shape=(7, 1), padding_x=(0.1, 0.1), color=(0.6, 0.6, 0.6, 1))

        self.trained_models_widget = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.trained_models_scroll.add_widget(self.trained_models_widget)
        self.trained_models_widget.bind(minimum_height=self.trained_models_widget.setter('height'))

        EventListener.add_listener("update_trained_models", self.update_trained_model_entries)

        self.editor_controls = SparseGridLayout(rows=1, cols=4)
        self.add_entry(self.editor_controls, position=(10, 0), shape=(1, 1), padding_x=(0.1, 0.1))

        self.close_button = Button(text="Close")
        self.close_button.on_press = self.close_trained_model
        self.editor_controls.add_entry(self.close_button, position=(0, 3), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1))
        self.editor_controls.hide_entry(self.close_button)

        self.result_viewer = TrainingResultView(self.audio_manager, self.execution_manager, self.trained_model_manager)
        self.add_entry(self.result_viewer, position=(0, 0), shape=(10, 1))
        self.hide_entry(self.result_viewer)

        self.update_trained_model_entries()

    def update_trained_model_entries(self):
        self.trained_models_widget.clear_widgets()
        for trained_model_id in self.execution_manager.all_trained_model_ids():
            is_open = trained_model_id == self.result_viewer.active_trained_model_id
            is_training = trained_model_id in self.execution_manager.active_trainers
            trained_entry = TrainedModelEntry(trained_model_id, is_open, is_training, self.execution_manager, self.trained_model_manager, self.open_trained_model, self.check_hide_delete)
            self.trained_models_widget.add_widget(trained_entry)

    def check_hide_delete(self, trained_model_id):
        if trained_model_id == self.result_viewer.active_trained_model_id:
            self.result_viewer.active_trained_model_id = None
            self.result_viewer.trained_model_result = None
            self.hide_entry(self.result_viewer)

    def update_active_trained_model_id(self, trained_model_id):
        if trained_model_id is None:
            self.hide_entry(self.result_viewer)
            self.result_viewer.active_trained_model_id = None
        else:
            self.result_viewer.update_active_trained_model_id(trained_model_id)
            self.show_entry(self.result_viewer)
        self.update_trained_model_entries()

    def open_trained_model(self, trained_model_id):
        self.update_active_trained_model_id(trained_model_id)
        self.editor_controls.show_entry(self.close_button)

    def close_trained_model(self):
        self.update_active_trained_model_id(None)
        self.editor_controls.hide_entry(self.close_button)
