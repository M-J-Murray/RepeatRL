from app.gui.util.sparse_grid_layout import SparseGridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from app.training.model.trained_model_manager import TrainedModelManager
from app.training.execution_manager import ExecutionManager
from app.audio.audio_manager import AudioManager
from functools import partial
from app.event_listener import EventListener


class TrainingResultView(SparseGridLayout):

    def __init__(self, audio_manager: AudioManager, execution_manager: ExecutionManager, trained_model_manager: TrainedModelManager):
        self.audio_manager = audio_manager
        self.execution_manager = execution_manager
        self.trained_model_manager = trained_model_manager
        self.active_trained_model_id = None
        self.trained_model = None
        self.train_stats = None

        super().__init__(rows=6, cols=2)

        self.background = Label()
        self.add_entry(self.background, position=(0, 0), shape=(6, 2), padding_x=(0.01, 0.01), padding_y=(0, 0.01), color=(0.3, 0.3, 0.3, 1))

        self.add_entry(Label(text='Model Results', font_size='15sp', color=[1, 1, 1, 1], bold=True), position=(5, 0), shape=(1, 2))

        self.add_entry(Label(text="Model ID:", font_size='15sp', color=[0., 0., 0., 1.]), position=(4, 0), shape=(1, 1))
        self.model_id = Label(text="", font_size='15sp', color=[0., 0., 0., 1.])
        self.add_entry(self.model_id, position=(4, 1), shape=(1, 1))

        self.add_entry(Label(text="Training ID:", font_size='15sp', color=[0., 0., 0., 1.]), position=(3, 0), shape=(1, 1))
        self.training_id = Label(text="", font_size='15sp', color=[0., 0., 0., 1.])
        self.add_entry(self.training_id, position=(3, 1), shape=(1, 1))

        self.add_entry(Label(text="Iterations: ", font_size='15sp', color=[0., 0., 0., 1.]), position=(2, 0), shape=(1, 1))
        self.iterations = Label(text="", font_size='15sp', color=[0., 0., 0., 1.])
        self.add_entry(self.iterations, position=(2, 1), shape=(1, 1))

        self.add_entry(Label(text="Accuracy: ", font_size='15sp', color=[0., 0., 0., 1.]), position=(1, 0), shape=(1, 1))
        self.accuracy = Label(text="", font_size='15sp', color=[0., 0., 0., 1.])
        self.add_entry(self.accuracy, position=(1, 1), shape=(1, 1))

        self.start_training_button = Button(text="Test Audio")
        self.start_training_button.bind(on_press=self.test_model_against_audio)
        self.add_entry(self.start_training_button, position=(0, 0.4), shape=(1, 0.8), padding_x=(0, 0.1), padding_y=(0.03, 0.03))

        self.audio_button = Button(text='Choose audio', size_hint=(None, None))
        self.audio_dropdown = DropDown(auto_width=False)
        self.audio_options = GridLayout(cols=1, spacing=0, size_hint_y=None, width=100)
        self.audio_options.bind(minimum_height=self.audio_options.setter('height'))
        self.audio_scroll = ScrollView(size_hint_y=None, height=100)
        with self.audio_scroll.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.audio_scroll.pos, size=self.audio_scroll.size)
        self.audio_scroll.add_widget(self.audio_options)
        self.audio_dropdown.add_widget(self.audio_scroll)
        self.audio_button.bind(on_release=self.audio_dropdown.open)
        self.add_entry(self.audio_button, position=(0, 1), shape=(1, 0.8), padding_x=(0, 0.1), padding_y=(0.03, 0.03))
        self.selected_audio_id = None

        self.update_audio_entries()
        EventListener.add_listener("update_audio_entries", self.update_audio_entries)

    def update_audio_entries(self):
        self.audio_options.clear_widgets()
        for audio_id in self.audio_manager.all_audio_ids():
            label = Label(text=audio_id, pos=(0, 0), height=20, size_hint=(1, None), color=(0, 0, 0, 1))
            label.on_touch_down = partial(self.update_audio_id, label)
            self.audio_options.add_widget(label)

    def update_audio_id(self, label, touch):
        if label.collide_point(*touch.pos):
            self.audio_dropdown.select(label.text)
            self.audio_button.text = label.text
            self.selected_audio_id = label.text

    def update_active_trained_model_id(self, trained_model_id):
        self.active_trained_model_id = trained_model_id
        trained_model, train_stats = self.trained_model_manager.load_trained_model(trained_model_id)
        self.trained_model = trained_model
        self.train_stats = train_stats
        training_model_split = trained_model_id.split("-")
        self.model_id.text = training_model_split[0]
        self.training_id.text = training_model_split[1]
        self.iterations.text = str(len(self.train_stats.results))
        self.accuracy.text = str(self.train_stats.best)

    def test_model_against_audio(self):
        pass
