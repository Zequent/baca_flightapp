from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.properties import BooleanProperty

class ZequentConnectionButton(MDFillRoundFlatIconButton):
    enabled = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def build(self):
        pass

    def on_press(self):
        self.enabled = not self.enabled

    def on_enabled(self, instance, *args):
        #print(self.enabled)
        pass
        
