from kivy.uix.stacklayout import StackLayout
from kivymd.app import MDApp

class ZequentStackLayout(StackLayout):

   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()

    def build(self):
        pass
        