from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp

class ZequentFloatLayout(FloatLayout):

   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()

    def build(self):
        pass
        