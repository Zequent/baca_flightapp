from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.uix.widget import Widget

class ZequentToast(Widget):

    zequentToast = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @staticmethod
    def showInfoMessage(message):
        toast(message)

    @staticmethod
    def showErrorMessage(message):
        toast(message)

    @staticmethod
    def showSuccessMessage(message):
        toast(message)

    def build(self):
        pass