from kivy.uix.boxlayout import BoxLayout
import tools.i18n as i18n
from tools.Globals import *

from kivymd.app import MDApp

class MainControllerLayout(BoxLayout):
    
    translator = i18n.Translator(Globals.getTranslatorFolder())
    welcomeText = translator.translate('welcome')
    app=MDApp.get_running_app()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        pass
        
