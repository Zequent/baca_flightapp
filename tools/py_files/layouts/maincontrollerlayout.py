from kivy.clock import Clock

from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.Utils import *
from kivymd.app import MDApp

class MainControllerLayout(ZequentBoxLayout):
    
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        """
        self.drone: ArduPlaneObject =self.app.drone
        print(self.app.drone.get_current_pos())
        Clock.schedule_interval(self.test, 3)
        """
    

    def build(self):
        pass

    def test(self, *args):
        print(self.app.drone.get_current_pos())
        print(self.app.drone.get_heartbeat())
        print(self.drone.ipAddress)
