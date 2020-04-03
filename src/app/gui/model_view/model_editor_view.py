from app.gui.util.sparse_grid_layout import SparseGridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from app.training.model.model_manager import ModelManager
import re
from app.event_listener import EventListener


class ModelEditorView(SparseGridLayout):

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.active_model = None
        self.model_definition = None

        super().__init__(rows=9, cols=1)

        self.background = Label()
        self.add_entry(self.background, position=(0, 0), shape=(9, 1), padding_x=(0.01, 0.01), padding_y=(0, 0.01), color=(0.3, 0.3, 0.3, 1))

        self.add_entry(Label(text='Model Editor', font_size='15sp', color=[1, 1, 1, 1], bold=True), position=(8, 0), shape=(1, 1))

        self.encoder_layout = SparseGridLayout(rows=2, cols=4)
        self.encoder_layout.add_entry(Label(text="Encoder", font_size='15sp', bold=True, color=[0., 0., 0., 1.]), position=(1, 0), shape=(1, 1))
        self.encoder_layout.add_entry(Label(text="LSTM Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 0), shape=(1, 1))
        self.enc_lstm_arch = TextInput(text="", multiline=False)
        self.enc_lstm_arch.bind(focus=self.update_enc_lstm_arch)
        self.encoder_layout.add_entry(self.enc_lstm_arch, position=(0, 1), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.encoder_layout.add_entry(Label(text="Tail Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 2), shape=(1, 1))
        self.enc_tail_arch = TextInput(text="", multiline=False)
        self.enc_tail_arch.bind(focus=self.update_enc_tail_arch)
        self.encoder_layout.add_entry(self.enc_tail_arch, position=(0, 3), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.add_entry(self.encoder_layout, position=(6, 0), shape=(3, 1))

        self.memory_layout = SparseGridLayout(rows=2, cols=6)
        self.memory_layout.add_entry(Label(text="Memory", font_size='15sp', bold=True, color=[0., 0., 0., 1.]), position=(1, 0), shape=(1, 1.5))
        self.memory_layout.add_entry(Label(text="Hidden:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 0), shape=(1, 1))
        self.mem_hidden = TextInput(text="", multiline=False)
        self.mem_hidden.bind(focus=self.update_mem_hidden)
        self.memory_layout.add_entry(self.mem_hidden, position=(0, 1), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.memory_layout.add_entry(Label(text="Loop:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 2), shape=(1, 1))
        self.mem_loop = TextInput(text="", multiline=False)
        self.mem_loop.bind(focus=self.update_mem_loop)
        self.memory_layout.add_entry(self.mem_loop, position=(0, 3), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.memory_layout.add_entry(Label(text="Tail Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 4), shape=(1, 1))
        self.mem_tail_arch = TextInput(text="", multiline=False)
        self.mem_tail_arch.bind(focus=self.update_mem_tail_arch)
        self.memory_layout.add_entry(self.mem_tail_arch, position=(0, 5), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.add_entry(self.memory_layout, position=(3, 0), shape=(3, 1))

        self.decoder_layout = SparseGridLayout(rows=2, cols=4)
        self.decoder_layout.add_entry(Label(text="Decoder", font_size='15sp', bold=True, color=[0., 0., 0., 1.]), position=(1, 0), shape=(1, 1))
        self.decoder_layout.add_entry(Label(text="LSTM Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 0), shape=(1, 1))
        self.dec_lstm_arch = TextInput(text="", multiline=False)
        self.dec_lstm_arch.bind(focus=self.update_dec_lstm_arch)
        self.decoder_layout.add_entry(self.dec_lstm_arch, position=(0, 1), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.decoder_layout.add_entry(Label(text="Tail Arch:", font_size='15sp', color=[0., 0., 0., 1.]), position=(0, 2), shape=(1, 1))
        self.dec_tail_arch = TextInput(text="", multiline=False)
        self.dec_tail_arch.bind(focus=self.update_dec_tail_arch)
        self.decoder_layout.add_entry(self.dec_tail_arch, position=(0, 3), shape=(1, 1), padding_x=(0, 0.02), padding_y=(0.1, 0.1))
        self.add_entry(self.decoder_layout, position=(0, 0), shape=(3, 1))

        self.csv_validator = re.compile(r"^(\d+,?)+$")
        self.int_validator = re.compile(r"^\d+$")

    def update_active_model(self, new_model_id):
        self.active_model = new_model_id
        self.model_definition = self.model_manager.load_model(self.active_model)
        self.enc_lstm_arch.text = ', '.join(map(str, self.model_definition.encoder_definition.lstm_arch))
        self.enc_tail_arch.text = ', '.join(map(str, self.model_definition.encoder_definition.tail_arch))
        self.mem_hidden.text = str(self.model_definition.memory_definition.hidden_n)
        self.mem_loop.text = str(self.model_definition.memory_definition.loop_n)
        self.mem_tail_arch.text = ', '.join(map(str, self.model_definition.memory_definition.tail_arch))
        self.dec_lstm_arch.text = ', '.join(map(str, self.model_definition.decoder_definition.lstm_arch))
        self.dec_tail_arch.text = ', '.join(map(str, self.model_definition.decoder_definition.tail_arch))

    def update_enc_lstm_arch(self, instance, value):
        if not value:
            clean = self.enc_lstm_arch.text.replace(" ", "")
            if not bool(self.csv_validator.match(clean)):
                raise Exception("Invalid encoder lstm arch")
            self.model_definition.encoder_definition.lstm_arch = str.split(clean, ",")
            self.update_model()

    def update_enc_tail_arch(self, instance, value):
        if not value:
            clean = self.enc_tail_arch.text.replace(" ", "")
            if not bool(self.csv_validator.match(clean)):
                raise Exception("Invalid encoder tail arch")
            self.model_definition.encoder_definition.tail_arch = str.split(clean, ",")
            self.update_model()

    def update_mem_hidden(self, instance, value):
        if not value:
            clean = self.mem_hidden.text.replace(" ", "")
            if not bool(self.int_validator.match(clean)):
                raise Exception("Invalid memory hidden")
            self.model_definition.memory_definition.hidden_n = int(clean)
            self.update_model()

    def update_mem_loop(self, instance, value):
        if not value:
            clean = self.mem_loop.text.replace(" ", "")
            if not bool(self.int_validator.match(clean)):
                raise Exception("Invalid memory loop")
            self.model_definition.memory_definition.loop_n = int(clean)
            self.update_model()

    def update_mem_tail_arch(self, instance, value):
        if not value:
            clean = self.mem_tail_arch.text.replace(" ", "")
            if not bool(self.csv_validator.match(clean)):
                raise Exception("Invalid memory tail arch")
            self.model_definition.memory_definition.tail_arch = str.split(clean, ",")
            self.update_model()

    def update_dec_lstm_arch(self, instance, value):
        if not value:
            clean = self.dec_lstm_arch.text.replace(" ", "")
            if not bool(self.csv_validator.match(clean)):
                raise Exception("Invalid decoder lstm arch")
            self.model_definition.decoder_definition.lstm_arch = str.split(clean, ",")
            self.update_model()

    def update_dec_tail_arch(self, instance, value):
        if not value:
            clean = self.dec_tail_arch.text.replace(" ", "")
            if not bool(self.csv_validator.match(clean)):
                raise Exception("Invalid decoder tail arch")
            self.model_definition.decoder_definition.tail_arch = str.split(clean, ",")
            self.update_model()

    def update_model(self):
        self.model_manager.update_model(self.active_model, self.model_definition)
        EventListener.trigger_event("refresh_model_definitions")
