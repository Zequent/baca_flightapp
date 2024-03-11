import traceback
from kivy.clock import Clock

from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.Utils import *
from kivymd.app import MDApp
from zequentmavlinklib.ArduPlane import ArduPlaneObject
import threading
import time

from tools.py_files.layouts.zequentcameralayout import ZequentCameraLayout
class MainControllerLayout(ZequentBoxLayout):
    
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.drone: ArduPlaneObject =self.app.drone
        #thread = threading.Thread(target=self.test2)
        #thread. threading.Timer(1, self.test).start()
        threading.Thread(target=lambda: self.every(1, self.test)).start()
       # thread.start()
        #thread.join()
        print("fuck off thread is finished")
        arm_msg = self.drone.arm()
        print(arm_msg)

    def build(self):
        pass


    def every(self, delay, task):
        next_time = time.time() + delay
        while True:
            time.sleep(max(0, next_time - time.time()))
            try:
                task()
            except Exception:
                traceback.print_exc()
            # in production code you might want to have this instead of course:
            # logger.exception("Problem while executing repetitive task.")
            # skip tasks if we are behind schedule:
            next_time += (time.time() - next_time) // delay * delay + delay


    def test(self):
        print("------------------TASK------------------------")
        response = self.drone.get_current_pos()
        lat = response.lat * 0.0000001
        lon = response.lon * 0.0000001
        print(self.drone.get_current_pos())
        print(self.drone.get_heartbeat())
        for child in self.ids.zequent_float_layout.children:
            if isinstance(child, ZequentCameraLayout):
                #print(child.ids)
                child.ids.mapview.change_marker(lat, lon)

       # print(self.drone.ipAddress)
