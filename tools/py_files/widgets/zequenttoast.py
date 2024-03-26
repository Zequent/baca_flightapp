from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.uix.widget import Widget
from kivy.clock import mainthread

class ZequentToast(Widget):

    zequentToast = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @staticmethod
    @mainthread
    def showInfoMessage(message):
        toast(message)

    @staticmethod
    @mainthread
    def showErrorMessage(message):
        toast(message)

    @staticmethod
    @mainthread
    def showSuccessMessage(message):
        toast(message)

    def build(self):
        pass