from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp

class ZequentAnchorLayout(AnchorLayout):

   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()

    def build(self):
        pass
        