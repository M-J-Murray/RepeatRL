from app.gui.util.sparse_grid_layout import SparseGridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from app.training.model.model_manager import ModelManager
from app.training.training_manager import TrainingManager
from app.training.execution_manager import ExecutionManager
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle
from app.event_listener import EventListener

from functools import partial
import re


class TrainingEditorView(SparseGridLayout):

    def __init__(self, model_manager: ModelManager, training_manager: TrainingManager, execution_manager: ExecutionManager):
        self.model_manager = model_manager
        self.training_manager = training_manager
        self.execution_manager = execution_manager
        self.active_training = None
        self.training_definition = None

        super().__init__(rows=6, cols=2)

        self.background = Label()
        self.add_entry(self.background, position=(0, 0), shape=(6, 2), padding_x=(0.01, 0.01), padding_y=(0, 0.01), color=(0.3, 0.3, 0.3, 1))

        self.add_entry(Label(text='Training Editor', font_size='15sp', color=[1, 1, 1, 1], bold=True), position=(5, 0), shape=(1, 2))

        self.add_entry(Label(text="Model ID:", font_size='15sp', color=[0., 0., 0., 1.]), position=(4, 0), shape=(1, 1))
        self.models_button = Button(text='Choose model', size_hint=(None, None))
        self.models_dropdown = DropDown(auto_width=False)
        self.models_options = GridLayout(cols=1, spacing=0, size_hint_y=None, width=100)
        self.models_options.bind(minimum_height=self.models_options.setter('height'))
        self.models_scroll = ScrollView(size_hint_y=None, height=100)
        with self.models_scroll.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.models_scroll.pos, size=self.models_scroll.size)
        self.models_scroll.add_widget(self.models_options)
        self.models_dropdown.add_widget(self.models_scroll)
        self.models_button.bind(on_release=self.models_dropdown.open)
        self.add_entry(self.models_button, position=(4, 1), shape=(1, 1), padding_x=(0, 0.1), padding_y=(0.03, 0.03))

        self.add_entry(Label(text="Learning Rate:", font_size='15sp', color=[0., 0., 0., 1.]), position=(3, 0), shape=(1, 1))
        self.learning_rate = TextInput(text="", multiline=False)
        self.learning_rate.bind(focus=self.update_learning_rate)
        self.add_entry(self.learning_rate, position=(3, 1), shape=(1, 1), padding_x=(0, 0.1), padding_y=(0.03, 0.03))

        self.add_entry(Label(text="Test Split:", font_size='15sp', color=[0., 0., 0., 1.]), position=(2, 0), shape=(1, 1))
        self.test_split = TextInput(text="", multiline=False)
        self.test_split.bind(focus=self.update_test_split)
        self.add_entry(self.test_split, position=(2, 1), shape=(1, 1), padding_x=(0, 0.1), padding_y=(0.03, 0.03))

        self.add_entry(Label(text="Iterations:", font_size='15sp', color=[0., 0., 0., 1.]), position=(1, 0), shape=(1, 1))
        self.iterations = TextInput(text="", multiline=False)
        self.iterations.bind(focus=self.update_iterations)
        self.add_entry(self.iterations, position=(1, 1), shape=(1, 1), padding_x=(0, 0.1), padding_y=(0.03, 0.03))

        self.start_training_button = Button(text="Start Training")
        self.start_training_button.bind(on_press=self.start_training)
        self.add_entry(self.start_training_button, position=(0, 0.6), shape=(1, 1), padding_x=(0, 0.1), padding_y=(0.03, 0.03))

        EventListener.add_listener("refresh_training_models", self.update_model_entries)

        self.float_regex = re.compile(r"^\d+(.\d+)?$")
        self.int_regex = re.compile(r"^\d+$")

        self.update_model_entries()

    def update_model_entries(self):
        self.models_options.clear_widgets()
        for model_id in self.model_manager.model_files:
            label = Label(text=model_id, pos=(0, 0), height=20, size_hint=(1, None), color=(0, 0, 0, 1))
            label.on_touch_down = partial(self.update_model_id, label)
            self.models_options.add_widget(label)

    def update_active_training(self, new_training_id):
        self.active_training = new_training_id
        self.training_definition = self.training_manager.load_training(self.active_training)
        if self.training_definition.model_id is None:
            self.models_button.text = "Choose model"
        else:
            self.models_button.text = self.training_definition.model_id
        self.learning_rate.text = str(self.training_definition.learning_rate)
        self.test_split.text = str(self.training_definition.test_split)
        self.iterations.text = str(self.training_definition.iterations)
        self.update_start_button()

    def update_start_button(self):
        if self.active_training in self.training_manager.unsaved_training or self.training_definition.model_id is None:
            self.hide_entry(self.start_training_button)
        else:
            self.show_entry(self.start_training_button)
        self.start_training_button.disabled = self.active_training in self.execution_manager.active_workers

    def update_model_id(self, label, touch):
        if label.collide_point(*touch.pos):
            self.models_dropdown.select(label.text)
            self.models_button.text = label.text
            if label.text != self.training_definition.model_id:
                self.training_definition.model_id = label.text
                self.update_definition()

    def update_learning_rate(self, instance, value):
        if not value:
            clean = self.learning_rate.text.replace(" ", "")
            if not bool(self.float_regex.match(clean)):
                raise Exception("Invalid learning rate")
            new_val = float(clean)
            if new_val != self.training_definition.learning_rate:
                self.training_definition.learning_rate = new_val
                self.update_definition()

    def update_test_split(self, instance, value):
        if not value:
            clean = self.test_split.text.replace(" ", "")
            if not bool(self.float_regex.match(clean)):
                raise Exception("Invalid learning rate")
            new_val = float(clean)
            if new_val != self.training_definition.test_split:
                self.training_definition.test_split = new_val
                self.update_definition()

    def update_iterations(self, instance, value):
        if not value:
            clean = self.iterations.text.replace(" ", "")
            if not bool(self.int_regex.match(clean)):
                raise Exception("Invalid learning rate")
            new_val = int(clean)
            if new_val != self.training_definition.iterations:
                self.training_definition.iterations = new_val
                self.update_definition()

    def update_definition(self):
        self.training_manager.update_training(self.active_training, self.training_definition)
        self.update_start_button()
        EventListener.trigger_event("refresh_training_view")

    def start_training(self, instance):
        instance.disabled = True
        self.execution_manager.start_training(self.active_training)
