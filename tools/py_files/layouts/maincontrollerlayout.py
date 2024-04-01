from functools import partial
import traceback
from kivy.clock import Clock

from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.Utils import *
from kivymd.app import MDApp
from zequentmavlinklib.ArduPlane import ArduPlaneObject
import threading
from tools.Utils import *
from tools.py_files.widgets.zequentmapview import ZequentMapView

logging.basicConfig(level=logging.DEBUG)
class MainControllerLayout(ZequentBoxLayout):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.app.connected = True
        self.drone: ArduPlaneObject =self.app.drone
        self.start_get_pos_thread()
        #self.start_get_stats_thread()
        #self.update_drone_states_worker()



    def start_get_pos_thread(self):
        update_pos_thread = WorkerThread(method=self.get_pos_worker,
                                          name="Position Update Worker", args=())
        update_pos_thread.start()

    def start_get_stats_thread(self):
        update_drone_stats = WorkerThread(method=self.get_states_from_drone, 
                                          name="Update Drone Stats", args=())
        update_drone_stats.start()



    def build(self):
        pass


    def update_drone_states_worker(self):
        if self.drone is not None:
            Utils.every(4, self.start_get_stats_thread)
            
      

    def get_states_from_drone(self):
        if self.drone is not None:
            self.drone.is_vehicle_armed()
            self.drone.get_battery_status()
            print("" + str(self.drone.is_armed) + "           " + str(self.drone.battery))
            self.ids.fix_tele_logs.is_armed = str(self.drone.is_armed)
            self.ids.fix_tele_logs.battery = str(self.drone.battery)


    def get_pos_worker(self):
        if self.drone is not None:
             Utils.every(1/30, self.get_current_pos_from_drone)

    def get_current_pos_from_drone(self):
        if self.drone is not None:
            response = self.drone.get_position()
            lat = response.lat * 0.0000001
            lon = response.lon * 0.0000001
            hdg = response.hdg / 100
            mapview: ZequentMapView = self.ids.camera_layout.ids.mapview 
            Clock.schedule_once(partial(mapview.change_pos_marker, lat, lon, hdg))
           