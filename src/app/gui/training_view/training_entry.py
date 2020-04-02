from app.gui.util.sparse_grid_layout import SparseGridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from app.training.training_manager import TrainingManager


class TrainingEntry(SparseGridLayout):

    def __init__(self, training_id, is_active, training_manager: TrainingManager, open_callback, save_callback, delete_callback, rename_callback):
        super().__init__(rows=1, cols=6, size_hint_y=None, height=40)
        self.training_id = training_id
        self.training_manager = training_manager
        self.open_callback = open_callback
        self.save_callback = save_callback
        self.delete_callback = delete_callback
        self.rename_callback = rename_callback

        background_color = (0.3, 0.3, 0.3, 1)
        if is_active:
            background_color = (0.3, 0.3, 0.6, 1)
        self.background = Label(padding_x=10)
        self.add_entry(self.background, position=(0, 0), shape=(1, 6), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05), color=background_color)

        self.training_label = Label(text=training_id, halign="left", valign="middle", padding_x=10)
        self.training_label.bind(size=self.training_label.setter('text_size'))
        self.training_label.on_touch_down = self.on_label_press
        self.add_entry(self.training_label, position=(0, 0), shape=(1, 3), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05))

        if training_id in self.training_manager.unsaved_training:
            self.save_button = Button(text="Save")
            self.save_button.on_press = self.save_training
            self.add_entry(self.save_button, position=(0, 3), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

        self.open_button = Button(text="Open")
        self.open_button.on_press = self.open_training
        self.add_entry(self.open_button, position=(0, 4), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

        self.delete_button = Button(text="Delete")
        self.delete_button.on_press = self.delete_training
        self.add_entry(self.delete_button, position=(0, 5), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

    def open_training(self):
        self.update_color(self.background, (0.3, 0.3, 0.6, 1))
        self.open_callback()

    def on_label_press(self, touch):
        if self.training_label.collide_point(*touch.pos):
            self.remove_entry(self.training_label)
            self.training_label = TextInput(text=self.training_id, multiline=False)
            self.training_label.bind(focus=self.update_training_label)
            self.training_label.on_touch_down(touch)
            self.add_entry(self.training_label, position=(0, 0), shape=(1, 3), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05))

    def update_training_label(self, instance, value):
        if not value:
            new_id = self.training_label.text
            self.remove_entry(self.training_label)
            if new_id != self.training_id:
                self.training_manager.rename_training(self.training_id, new_id)
                self.rename_callback(self.training_id, self.new_id)
                self.training_id = new_id
            self.training_label = Label(text=self.training_id, halign="left", valign="middle", padding_x=10)
            self.training_label.bind(size=self.training_label.setter('text_size'))
            self.training_label.on_touch_down = self.on_label_press
            self.add_entry(self.training_label, position=(0, 0), shape=(1, 3), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05))

    def save_training(self):
        self.training_manager.save_training(self.training_id)
        self.remove_widget(self.save_button)
        self.save_callback(self.training_id)

    def delete_training(self):
        self.training_manager.delete_training(self.training_id)
        self.parent.remove_widget(self)
        self.delete_callback(self.training_id)
