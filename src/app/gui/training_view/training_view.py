from app.gui.util.sparse_grid_layout import SparseGridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from app.gui.training_view.training_editor_view import TrainingEditorView
from app.gui.training_view.training_entry import TrainingEntry

from app.event_listener import EventListener

from kivy.uix.label import Label
from kivy.uix.button import Button


class TrainingView(SparseGridLayout):

    def __init__(self, audio_manager, model_manager, training_manager, execution_manager):
        self.audio_manager = audio_manager
        self.model_manager = model_manager
        self.training_manager = training_manager
        self.execution_manager = execution_manager
        super().__init__(rows=20, cols=1)
        self.add_entry(Label(text='Training', font_size='20sp', color=[0, 0, 0, 1]), position=(18, 0), shape=(2, 1))

        self.training_scroll = ScrollView()
        self.add_entry(self.training_scroll, position=(11, 0), shape=(7, 1), padding_x=(0.1, 0.1), color=(0.6, 0.6, 0.6, 1))

        self.training_widget = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.training_scroll.add_widget(self.training_widget)
        self.training_widget.bind(minimum_height=self.training_widget.setter('height'))

        self.editor_controls = SparseGridLayout(rows=1, cols=3)
        self.add_entry(self.editor_controls, position=(10, 0), shape=(1, 1), padding_x=(0.1, 0.1))

        self.new_button = Button(text="New")
        self.new_button.on_press = self.new_training
        self.editor_controls.add_entry(self.new_button, position=(0, 0), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1))

        self.save_button = Button(text="Save")
        self.save_button.on_press = self.save_training
        self.editor_controls.add_entry(self.save_button, position=(0, 1), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1))
        self.editor_controls.hide_entry(self.save_button)

        self.close_button = Button(text="Close")
        self.close_button.on_press = self.close_training
        self.editor_controls.add_entry(self.close_button, position=(0, 2), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1))
        self.editor_controls.hide_entry(self.close_button)

        self.training_editor = TrainingEditorView(self.model_manager, self.training_manager, self.execution_manager)
        EventListener.add_listener("refresh_training_view", self.update_training_definitions)
        self.add_entry(self.training_editor, position=(0, 0), shape=(10, 1))
        self.hide_entry(self.training_editor)

        self.update_training_definitions()

    def update_training_definitions(self):
        if self.training_editor.active_training is not None and self.training_editor.active_training in self.training_manager.unsaved_training:
            self.editor_controls.show_entry(self.save_button)
        else:
            self.editor_controls.hide_entry(self.save_button)
        self.training_widget.clear_widgets()
        for training_id in self.training_manager.all_training_ids():
            is_active = training_id == self.training_editor.active_training
            training_entry = TrainingEntry(training_id, is_active, self.training_manager, self.open_training, self.check_hide_save, self.check_hide_delete,
                                           self.check_update_editor_name)
            self.training_widget.add_widget(training_entry)

    def check_update_editor_name(self, old_id, new_id):
        if self.training_editor.active_training == old_id:
            self.training_editor.active_training = new_id

    def check_hide_delete(self, training_id):
        if training_id == self.training_editor.active_training:
            self.training_editor.active_training = None
            self.training_editor.training_definition = None
            self.hide_entry(self.training_editor)

    def check_hide_save(self, training_id):
        if training_id == self.training_editor.active_training:
            self.editor_controls.hide_entry(self.save_button)
            self.training_editor.update_start_button()

    def update_active_training(self, training_id):
        if training_id is None:
            self.hide_entry(self.training_editor)
            self.training_editor.active_training = None
        else:
            self.training_editor.update_active_training(training_id)
            self.show_entry(self.training_editor)
        self.update_training_definitions()

    def new_training(self):
        self.update_active_training(self.training_manager.new_training())
        self.editor_controls.show_entry(self.close_button)

    def save_training(self):
        self.training_manager.save_training(self.training_editor.active_training)
        self.training_editor.update_start_button()
        self.update_training_definitions()

    def open_training(self, training_id):
        self.update_active_training(training_id)
        self.editor_controls.show_entry(self.close_button)

    def close_training(self):
        self.update_active_training(None)
        self.editor_controls.hide_entry(self.close_button)
