from .linelayout import GUILayout


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
            if widget.base_height is not None:
                w_h = widget.base_height
            elif widget.height_hint is not None:
                w_h = int(widget.height_hint * self.height)
            else:
                w_h = widget.min_height

            if widget.base_width is not None:
                w_w = widget.base_width
            elif widget.width_hint is not None:
                w_w = int(widget.width_hint * self.width)
            else:
                w_w = widget.min_width

            widget.size = (w_w, w_h)
            widget.pos = (self.width * x_mod - widget.width * x_mod,
                          self.height * y_mod - widget.height * y_mod)

            min_w = max(min_w, widget.min_width)
            min_h = max(min_h, widget.min_height)

        self._min_size = (min_w, min_h)
