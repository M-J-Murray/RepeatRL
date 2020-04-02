from app.gui.util.sparse_grid_layout import SparseGridLayout
from app.gui.audio_view.audio_entry import AudioEntry
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from app.audio.audio_manager import AudioManager


class AudioView(SparseGridLayout):

    def __init__(self, audio_manager: AudioManager):
        super().__init__(rows=10, cols=1)
        self.audio_manager = audio_manager

        self.add_entry(Label(text='Audio Recordings', font_size='20sp', color=[0., 0., 0., 1.]), position=(9, 0),
                       shape=(1, 1))

        self.clip_scroll = ScrollView()
        self.add_entry(self.clip_scroll, position=(3, 0), shape=(6, 1), padding_x=(0.1, 0.1), color=(0.6, 0.6, 0.6, 1))

        self.clips_widget = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.clip_scroll.add_widget(self.clips_widget)
        self.clips_widget.bind(minimum_height=self.clips_widget.setter('height'))
        self.update_recording_entries()

        self.control_widget = SparseGridLayout(rows=2, cols=4)
        self.add_entry(self.control_widget, position=(0, 0), shape=(3, 1))

        self.record_button = Button(text="Record")
        self.record_button.on_press = self.record_callback
        self.control_widget.add_entry(self.record_button, position=(1, 1), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1))

        self.save_all_button = Button(text="Save All")
        self.save_all_button.on_press = self.save_all_callback
        self.control_widget.add_entry(self.save_all_button, position=(1, 2), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1))

    def update_recording_entries(self):
        self.clips_widget.clear_widgets()
        for audio_id in self.audio_manager.all_audio_ids():
            audio_entry = AudioEntry(audio_id, self.audio_manager)
            self.clips_widget.add_widget(audio_entry)

    def save_all_callback(self):
        self.audio_manager.save_all()
        self.update_recording_entries()

    def record_callback(self):
        self.record_button.on_press = self.stop_record_callback
        self.record_button.text = "Stop"
        self.audio_manager.start_recording()

    def stop_record_callback(self):
        self.record_button.on_press = self.record_callback
        self.record_button.text = "Record"
        self.audio_manager.stop_recording()
        self.update_recording_entries()
