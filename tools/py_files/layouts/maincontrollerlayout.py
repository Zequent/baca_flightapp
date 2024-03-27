import traceback
from kivy.clock import Clock as clock

from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.Utils import *
from kivymd.app import MDApp
from zequentmavlinklib.ArduPlane import ArduPlaneObject
from zequentmavlinklib.Globals import WorkerThread
import threading
from tools.Utils import *
from tools.py_files.widgets.zequentmapview import ZequentMapView
class MainControllerLayout(ZequentBoxLayout):
    
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.app.connected = True
        self.drone: ArduPlaneObject =self.app.drone
        if self.drone is not None:
            thread = threading.Thread(target=lambda: Utils.every(0.1, self.get_current_pos_from_drone))
            thread.start()

    def build(self):
        pass


    def get_current_pos_from_drone(self):
        if self.drone is not None:
            response = self.drone.get_position()
            #self.ids.row_logs.logs = str(response)

            lat = response.lat * 0.0000001
            lon = response.lon * 0.0000001
            hdg = response.hdg / 100
            mapview: ZequentMapView = self.ids.camera_layout.ids.mapview 
            mapview.change_pos_marker(lat, lon, hdg)
           