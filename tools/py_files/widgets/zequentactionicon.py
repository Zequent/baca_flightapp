from kivy.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.stacklayout import MDStackLayout

from tools.py_files.layouts.casuals.zequentboxlayout import *
from kivymd.uix.button import MDIconButton, MDFloatingActionButton
from tools.py_files.widgets.zequentlabel import *
from kivy.properties import ObjectProperty


class ZequentActionIcon(MDBoxLayout):
    icon = ObjectProperty(None)
    text = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.adaptive_size = True
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    def on_icon(self, instance, value):
        icon2 = MDFloatingActionButton(icon=value)
        icon2.icon = value
        icon2.type = 'small'
        icon2.md_bg_color = None
        self.add_widget(icon2)

    def on_text(self, instance, value):
        label = MDLabel(text=value, valign='top', halign='center')
        self.add_widget(label)

    def build(self):
        pass
