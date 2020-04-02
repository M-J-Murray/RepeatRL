from app.gui.util.sparse_grid_layout import SparseGridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from kivy.uix.label import Label


class TrainedModelView(SparseGridLayout):

    def __init__(self, audio_manager, model_manager, training_manager, trained_model_manager):
        self.audio_manager = audio_manager
        self.model_manager = model_manager
        self.training_manager = training_manager
        self.trained_model_manager = trained_model_manager
        super().__init__(rows=20, cols=1)
        self.add_entry(Label(text='Trained Models', font_size='20sp', color=[0, 0, 0, 1]), position=(18, 0), shape=(2, 1))

        self.models_scroll = ScrollView()
        self.add_entry(self.models_scroll, position=(11, 0), shape=(7, 1), padding_x=(0.1, 0.1), color=(0.6, 0.6, 0.6, 1))

        self.models_widget = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.models_scroll.add_widget(self.models_widget)
        self.models_widget.bind(minimum_height=self.models_widget.setter('height'))

