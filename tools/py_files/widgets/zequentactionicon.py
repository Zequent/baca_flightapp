from tools.py_files.layouts.casuals.zequentboxlayout import *
from kivymd.uix.button import MDIconButton
from tools.py_files.widgets.zequentlabel import *
from kivy.properties import ObjectProperty

class ZequentActionIcon(ZequentBoxLayout):
    
    icon= ObjectProperty(None)
    text= ObjectProperty(None)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint= None,1    
        self.spacing= 0
        self.padding= 0
    
    def on_icon(self, instance, value):
        icon = MDIconButton(
            icon=value,
            padding= 0
        )
        
        self.add_widget(icon)

    def on_text(self, instance, value):
        print(value)
        label = ZequentLabel(text=value)
        label.padding= 0

        self.add_widget(label)

        
        

    
    def build(self):
        pass