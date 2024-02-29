from tools.py_files.layouts.casuals.zequentgridlayout import *
from kivymd.app import MDApp
from tools.Utils import *

class ZequentRootLayout(ZequentGridLayout):
    app= MDApp.get_running_app()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def build(self):
        pass

   
    
   

    