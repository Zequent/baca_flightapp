from kivy.uix.scatterlayout import ScatterLayout
from kivymd.app import MDApp

class ZequentScatterLayout(ScatterLayout):

   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()

    def build(self):
        pass
        