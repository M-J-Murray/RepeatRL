from app.gui.util.sparse_grid_layout import SparseGridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from app.training.execution_manager import ExecutionManager
from app.training.model.trained_model_manager import TrainedModelManager


class TrainedModelEntry(SparseGridLayout):

    def __init__(self, trained_model_id, is_open, is_training, execution_manager: ExecutionManager, trained_model_manager: TrainedModelManager, open_callback, delete_callback):
        super().__init__(rows=1, cols=6, size_hint_y=None, height=40)
        self.trained_model_id = trained_model_id
        self.execution_manager = execution_manager
        self.trained_model_manager = trained_model_manager
        self.open_callback = open_callback
        self.delete_callback = delete_callback

        background_color = [0.3, 0.3, 0.3, 1]
        if is_open:
            background_color[0] += 0.1
            background_color[1] += 0.1
            background_color[2] += 0.1
        if is_training:
            background_color[0] += 0.3

        self.background = Label(padding_x=10)
        self.add_entry(self.background, position=(0, 0), shape=(1, 6), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05), color=background_color)

        self.trained_model_label = Label(text=trained_model_id, halign="left", valign="middle", padding_x=10)
        self.trained_model_label.bind(size=self.trained_model_label.setter('text_size'))
        self.add_entry(self.trained_model_label, position=(0, 0), shape=(1, 4), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05))

        self.open_button = Button(text="Open")
        self.open_button.on_press = self.open_trained_model
        self.add_entry(self.open_button, position=(0, 4), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

        self.delete_button = Button(text="Delete")
        self.delete_button.on_press = self.delete_trained_model
        self.add_entry(self.delete_button, position=(0, 5), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

    def open_trained_model(self):
        self.update_color(self.background, (0.3, 0.3, 0.6, 1))
        self.open_callback(self.trained_model_id)

    def delete_trained_model(self):
        self.trained_model_manager.delete_trained_model(self.trained_model_id)
        self.parent.remove_widget(self)
        self.delete_callback(self.trained_model_id)
