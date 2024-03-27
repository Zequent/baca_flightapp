from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.properties import BooleanProperty, ObjectProperty
from copy import copy

from matplotlib.animation import Animation
from kivy.uix.behaviors import ToggleButtonBehavior

class ZequentConnectionButton(MDFillRoundFlatIconButton):
    enabled = BooleanProperty(False)

    currObject = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ripple_scale=0
    
    def build(self):
        pass

    def on_press(self):
        self.enabled = not self.enabled
        

    def on_enabled(self, instance, *args):
        #print(self.enabled)
        pass
        
    def checkGrid(self,root, *args):
        if self.enabled == True:
            idx = self.parent.children.index(self)
            root.add_widget(self.currObject, idx-1)
        else:
            root.remove_widget(self.currObject)
            


