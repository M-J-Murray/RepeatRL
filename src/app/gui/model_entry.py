from app.gui.sparse_grid_layout import SparseGridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from app.training.model.model_manager import ModelManager


class ModelEntry(SparseGridLayout):

    def __init__(self, model_id, is_active, model_manager: ModelManager, open_callback, save_callback, delete_callback):
        super().__init__(rows=1, cols=6, size_hint_y=None, height=40)
        self.model_id = model_id
        self.model_manager = model_manager
        self.open_callback = open_callback
        self.save_callback = save_callback
        self.delete_callback = delete_callback

        background_color = (0.3, 0.3, 0.3, 1)
        if is_active:
            background_color = (0.3, 0.3, 0.6, 1)
        self.background = Label(padding_x=10)
        self.add_entry(self.background, position=(0, 0), shape=(1, 6), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05), color=background_color)

        self.model_label = Label(text=model_id, halign="left", valign="middle", padding_x=10)
        self.model_label.bind(size=self.model_label.setter('text_size'))
        self.model_label.on_touch_down = self.on_label_press
        self.add_entry(self.model_label, position=(0, 0), shape=(1, 3), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05))

        if model_id in self.model_manager.unsaved_models:
            self.save_button = Button(text="Save")
            self.save_button.on_press = self.save_model
            self.add_entry(self.save_button, position=(0, 3), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

        self.open_button = Button(text="Open")
        self.open_button.on_press = self.open_model
        self.add_entry(self.open_button, position=(0, 4), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

        self.delete_button = Button(text="Delete")
        self.delete_button.on_press = self.delete_model
        self.add_entry(self.delete_button, position=(0, 5), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

    def open_model(self):
        self.update_color(self.background, (0.3, 0.3, 0.6, 1))
        self.open_callback()

    def on_label_press(self, touch):
        if self.model_label.collide_point(*touch.pos):
            self.remove_entry(self.model_label)
            self.model_label = TextInput(text=self.model_id, multiline=False)
            self.model_label.bind(focus=self.update_model_label)
            self.model_label.on_touch_down(touch)
            self.add_entry(self.model_label, position=(0, 0), shape=(1, 3), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05), color=(0.3, 0.3, 0.3, 1))

    def update_model_label(self, instance, value):
        if not value:
            new_id = self.model_label.text
            self.remove_entry(self.model_label)
            if new_id != self.model_id:
                self.model_manager.rename_model(self.model_id, new_id)
                self.model_id = new_id
            self.model_label = Label(text=self.model_id, halign="left", valign="middle", padding_x=10)
            self.model_label.bind(size=self.model_label.setter('text_size'))
            self.model_label.on_touch_down = self.on_label_press
            self.add_entry(self.model_label, position=(0, 0), shape=(1, 3), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05), color=(0.3, 0.3, 0.3, 1))

    def save_model(self):
        self.model_manager.save_model(self.model_id)
        self.remove_widget(self.save_button)
        self.save_callback(self.model_id)

    def delete_model(self):
        self.model_manager.delete_model(self.model_id)
        self.parent.remove_widget(self)
        self.delete_callback(self.model_id)
