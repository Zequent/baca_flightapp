from kivy.uix.widget import Widget
from kivy.clock import mainthread
from kivymd.app import MDApp

class GraphicalChangeExecutor(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    @mainthread
    def execute(method):
        method()