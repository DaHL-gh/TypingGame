from .gui_object import GUILayout


class FloatLayout(GUILayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _update_layout(self) -> None:
        for widget in self._widgets:
            widget.pos = widget.pos