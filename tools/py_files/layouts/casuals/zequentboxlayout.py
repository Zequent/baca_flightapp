from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp

class ZequentBoxLayout(BoxLayout):

   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()

    def build(self):
        pass
        