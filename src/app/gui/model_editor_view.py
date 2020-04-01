from app.gui.sparse_grid_layout import SparseGridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from app.training.model.model_manager import ModelManager
from app.gui.model_entry import ModelEntry

from functools import partial


class ModelEditorView(SparseGridLayout):

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager

        super().__init__(rows=10, cols=1)

        self.background = Label()
        self.add_entry(self.background, position=(0, 0), shape=(9, 1), padding_x=(0.01, 0.01), padding_y=(0, 0.01), color=(0.3, 0.3, 0.3, 1))

        self.add_entry(Label(text='Model Editor', font_size='15sp', color=[0, 0, 0, 1], bold=True), position=(9, 0), shape=(1, 1))

        self.encoder_layout = SparseGridLayout(rows=2, cols=4)
        self.encoder_layout.add_entry(Label(text="Encoder", font_size='15sp', bold=True, color=[0., 0., 0., 1.]), position=(1, 1), shape=(1, 2))
        self.encoder_layout.add_entry(Label(text="LSTM Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 0), shape=(1, 1))
        self.enc_lstm_arch = TextInput(text="", multiline=False)
        self.encoder_layout.add_entry(self.enc_lstm_arch, position=(0, 1), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.encoder_layout.add_entry(Label(text="Tail Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 2), shape=(1, 1))
        self.enc_tail_arch = TextInput(text="", multiline=False)
        self.encoder_layout.add_entry(self.enc_tail_arch, position=(0, 3), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.add_entry(self.encoder_layout, position=(6, 0), shape=(3, 1))

        self.memory_layout = SparseGridLayout(rows=2, cols=6)
        self.memory_layout.add_entry(Label(text="Memory", font_size='15sp', bold=True, color=[0., 0., 0., 1.]), position=(1, 2), shape=(1, 2))
        self.memory_layout.add_entry(Label(text="Hidden:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 0), shape=(1, 1))
        self.mem_hidden = TextInput(text="", multiline=False)
        self.memory_layout.add_entry(self.mem_hidden, position=(0, 1), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.memory_layout.add_entry(Label(text="Loop:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 2), shape=(1, 1))
        self.mem_loop = TextInput(text="", multiline=False)
        self.memory_layout.add_entry(self.mem_loop, position=(0, 3), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.memory_layout.add_entry(Label(text="Tail Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 4), shape=(1, 1))
        self.mem_tail_arch = TextInput(text="", multiline=False)
        self.memory_layout.add_entry(self.mem_tail_arch, position=(0, 5), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.add_entry(self.memory_layout, position=(3, 0), shape=(3, 1))

        self.decoder_layout = SparseGridLayout(rows=2, cols=4)
        self.decoder_layout.add_entry(Label(text="Decoder", font_size='15sp', bold=True, color=[0., 0., 0., 1.]), position=(1, 1), shape=(1, 2))
        self.decoder_layout.add_entry(Label(text="LSTM Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 0), shape=(1, 1))
        self.dec_lstm_arch = TextInput(text="", multiline=False)
        self.decoder_layout.add_entry(self.dec_lstm_arch, position=(0, 1), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.decoder_layout.add_entry(Label(text="Tail Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 2), shape=(1, 1))
        self.dec_tail_arch = TextInput(text="", multiline=False)
        self.decoder_layout.add_entry(self.dec_tail_arch, position=(0, 3), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.add_entry(self.decoder_layout, position=(0, 0), shape=(3, 1))
