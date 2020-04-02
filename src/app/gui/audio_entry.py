from app.gui.sparse_grid_layout import SparseGridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from app.audio.audio_manager import AudioManager


class AudioEntry(SparseGridLayout):

    def __init__(self, audio_id, audio_manager: AudioManager):
        super().__init__(rows=1, cols=6, size_hint_y=None, height=40)
        self.audio_id = audio_id
        self.audio_manager = audio_manager

        self.background = Label(padding_x=10)
        self.add_entry(self.background, position=(0, 0), shape=(1, 6), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05), color=(0.3, 0.3, 0.3, 1))

        self.audio_label = Label(text=audio_id, halign="left", valign="middle", padding_x=10)
        self.audio_label.bind(size=self.audio_label.setter('text_size'))
        self.audio_label.on_touch_down = self.on_label_press
        self.add_entry(self.audio_label, position=(0, 0), shape=(1, 3), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05),)

        if audio_id in self.audio_manager.unsaved_audio:
            self.save_button = Button(text="Save")
            self.save_button.on_press = self.save_clip
            self.add_entry(self.save_button, position=(0, 3), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

        self.play_button = Button(text="Play")
        self.play_button.on_press = self.play_audio
        self.add_entry(self.play_button, position=(0, 4), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

        self.delete_button = Button(text="Delete")
        self.delete_button.on_press = self.delete_clip
        self.add_entry(self.delete_button, position=(0, 5), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1), index=10)

    def on_label_press(self, touch):
        if self.audio_label.collide_point(*touch.pos):
            self.remove_entry(self.audio_label)
            self.audio_label = TextInput(text=self.audio_id, multiline=False)
            self.audio_label.bind(focus=self.update_audio_label)
            self.audio_label.on_touch_down(touch)
            self.add_entry(self.audio_label, position=(0, 0), shape=(1, 3), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05), color=(0.3, 0.3, 0.3, 1))

    def update_audio_label(self, instance, value):
        if not value:
            new_id = self.audio_label.text
            self.remove_entry(self.audio_label)
            if new_id != self.audio_id:
                self.audio_manager.rename_audio(self.audio_id, new_id)
                self.audio_id = new_id
            self.audio_label = Label(text=self.audio_id, halign="left", valign="middle", padding_x=10)
            self.audio_label.bind(size=self.audio_label.setter('text_size'))
            self.audio_label.on_touch_down = self.on_label_press
            self.add_entry(self.audio_label, position=(0, 0), shape=(1, 3), padding_x=(0.01, 0.01), padding_y=(0.05, 0.05), color=(0.3, 0.3, 0.3, 1))

    def update_stop_to_play(self):
        self.play_button.text = "Play"
        self.play_button.on_press = self.play_audio

    def play_audio(self):
        self.audio_manager.play_audio(self.audio_id, on_complete=self.update_stop_to_play)
        self.play_button.text = "Stop"
        self.play_button.on_press = self.stop_audio

    def stop_audio(self):
        self.audio_manager.stop_audio()
        self.update_stop_to_play()

    def save_clip(self):
        self.audio_manager.save_audio(self.audio_id)
        self.remove_widget(self.save_button)

    def delete_clip(self):
        self.audio_manager.delete_audio(self.audio_id)
        self.parent.remove_widget(self)
