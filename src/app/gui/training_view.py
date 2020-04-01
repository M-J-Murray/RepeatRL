from app.gui.sparse_grid_layout import SparseGridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class TrainingView(SparseGridLayout):

    def __init__(self, audio_manager, model_manager, training_manager):
        self.audio_manager = audio_manager
        self.model_manager = model_manager
        self.training_manager = training_manager
        super().__init__(rows=10, cols=1)
        self.add_entry(Label(text='Training', font_size='20sp', color=[0, 0, 0, 1]), position=(9, 0), shape=(1, 1))

