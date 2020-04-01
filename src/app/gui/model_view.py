from app.gui.sparse_grid_layout import SparseGridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from app.training.model.model_manager import ModelManager
from app.gui.model_entry import ModelEntry
from app.gui.model_editor_view import ModelEditorView

from functools import partial


class ModelView(SparseGridLayout):

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager

        super().__init__(rows=20, cols=1)
        self.add_entry(Label(text='Models', font_size='20sp', color=[0, 0, 0, 1]), position=(18, 0), shape=(2, 1))

        self.models_scroll = ScrollView()
        self.add_entry(self.models_scroll, position=(11, 0), shape=(7, 1), padding_x=(0.1, 0.1), color=(0.6, 0.6, 0.6, 1))

        self.models_widget = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.models_scroll.add_widget(self.models_widget)
        self.models_widget.bind(minimum_height=self.models_widget.setter('height'))

        self.editor_controls = SparseGridLayout(rows=1, cols=3)
        self.add_entry(self.editor_controls, position=(10, 0), shape=(1, 1), padding_x=(0.1, 0.1))

        self.new_button = Button(text="New")
        self.new_button.on_press = self.new_model
        self.editor_controls.add_entry(self.new_button, position=(0, 0), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1))

        self.save_button = Button(text="Save")
        self.save_button.on_press = self.save_model
        self.editor_controls.add_entry(self.save_button, position=(0, 1), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1))

        self.close_button = Button(text="Close")
        self.close_button.on_press = self.close_model
        self.editor_controls.add_entry(self.close_button, position=(0, 2), shape=(1, 1), padding_x=(0.01, 0.01), padding_y=(0.1, 0.1))

        self.active_model = None
        self.model_editor = ModelEditorView(self.model_manager)
        self.add_entry(self.model_editor, position=(0, 0), shape=(10, 1))
        self.hide_entry(self.model_editor)

    def update_model_definitions(self):
        self.models_widget.clear_widgets()
        for model_id in self.model_manager.all_model_ids():
            model_entry = ModelEntry(model_id, self.model_manager, partial(self.open_model, model_id))
            self.models_widget.add_widget(model_entry)

    def update_active_model(self, model_id):
        self.active_model = model_id
        if model_id is None:
            self.hide_entry(self.model_editor)
        else:
            self.show_entry(self.model_editor)
        self.update_model_definitions()

    def new_model(self):
        self.update_active_model(self.model_manager.new_model())

    def save_model(self):
        pass

    def open_model(self, model_id):
        self.update_active_model(model_id)

    def close_model(self):
        self.update_active_model(None)
