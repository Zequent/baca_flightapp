from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.uix.widget import Widget

class ZequentToast(Widget):

    zequentToast = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zequentToast = toast
    
    def build(self):
        pass