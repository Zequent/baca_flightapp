from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp

class ZequentRelativeLayout(RelativeLayout):

   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()

    def build(self):
        pass
        