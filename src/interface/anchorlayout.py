from .gui_object import GUILayout


class AnchorLayout(GUILayout):
    def __init__(self, x_anchor='c', y_anchor='c', **kwargs):
        super().__init__(**kwargs)

        self._x_anchor = x_anchor  # l or c or r
        self._y_anchor = y_anchor  # t or c or b

    @property
    def x_anchor(self):
        return self._x_anchor

    @property
    def y_anchor(self):
        return self._y_anchor

    def _update_layout(self):
        if self.x_anchor == 'l':
            x_mod = 0
        elif self.x_anchor == 'c':
            x_mod = 0.5
        else:
            x_mod = 1

        if self.y_anchor == 't':
            y_mod = 0
        elif self.y_anchor == 'c':
            y_mod = 0.5
        else:
            y_mod = 1

        min_w = min_h = 0
        for widget in self._widgets:
            widget.pos = (self.width * y_mod - widget.width * y_mod,
                          self.height * x_mod - widget.height * x_mod)

            min_w = max(min_w, widget.width)
            min_h = max(min_h, widget.height)

        self._min_size = (min_w, min_h)
