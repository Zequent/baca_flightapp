from kivy.uix.pagelayout import PageLayout
from kivymd.app import MDApp

class ZequentPageLayout(PageLayout):

   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()

    def build(self):
        pass
        