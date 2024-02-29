from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp

class ZequentGridLayout(GridLayout):

   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()

    def build(self):
        pass
        