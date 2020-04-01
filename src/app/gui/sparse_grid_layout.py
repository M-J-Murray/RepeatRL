from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle


class SparseGridLayout(RelativeLayout):

    def __init__(self, rows, cols, **kwargs):
        super().__init__(**kwargs)

        self.rows = rows
        self.cols = cols
        self.children_position = dict()
        self.children_shape = dict()
        self.children_padding_x = dict()
        self.children_padding_y = dict()
        self.children_color = dict()
        self.child_rects = dict()
        self.children_visibility = dict()

    def do_layout(self, *args):
        shape_hint = (1. / self.rows, 1. / self.cols)
        for child in self.children:
            pos = self.children_position[child]
            shape = self.children_shape[child]
            padding_x = self.children_padding_x[child]
            padding_y = self.children_padding_y[child]
            color = self.children_color[child]
            child.pos_hint = {'x': (shape_hint[1] * pos[1]) + padding_x[0], 'y': (shape_hint[0] * pos[0]) + padding_y[1]}
            child.size_hint = ((shape_hint[1] * shape[1]) - (padding_x[0] + padding_x[1]), (shape_hint[0] * shape[0]) - (padding_y[0] + padding_y[1]))
            if child not in self.child_rects:
                with self.canvas.before:
                    Color(*color)
                    self.child_rects[child] = Rectangle(pos=child.pos, size=child.size)
                    child.bind(size=self.update_size, pos=self.update_pos)

        super(SparseGridLayout, self).do_layout(*args)

    def update_color(self, widget, new_color):
        self.children_color[widget] = new_color
        self.canvas.ask_update()

    def update_pos(self, instance, value):
        self.child_rects[instance].pos = value

    def update_size(self, instance, value):
        self.child_rects[instance].size = value

    def add_entry(self, widget, position, shape, padding_x=(0, 0), padding_y=(0, 0), color=(0, 0, 0, 0), index=0):
        super().add_widget(widget, index=index)
        self.children_position[widget] = position
        self.children_shape[widget] = shape
        self.children_padding_x[widget] = padding_x
        self.children_padding_y[widget] = padding_y
        self.children_color[widget] = color
        self.children_visibility[widget] = True

    def hide_entry(self, widget):
        if self.children_visibility[widget]:
            self.remove_widget(widget)
        self.children_visibility[widget] = False

    def show_entry(self, widget):
        if not self.children_visibility[widget]:
            self.add_widget(widget)
        self.children_visibility[widget] = True

    def remove_entry(self, widget):
        super().remove_widget(widget)
        del self.children_position[widget]
        del self.children_shape[widget]
        del self.children_padding[widget]
        del self.children_color[widget]
