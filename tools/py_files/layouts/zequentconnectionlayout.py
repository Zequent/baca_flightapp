from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.py_files.layouts.casuals.zequentanchorlayout import *
from tools.py_files.layouts.casuals.zequentgridlayout import *
from kivy.clock import Clock
from functools import partial
from kivymd.app import MDApp
from tools.Utils import *




class ZequentConnectionLayout(ZequentGridLayout):
    
    connectionStatusText = ''


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def build(self):
        self.connectionStatusText = self.root.ids.translator.translate('not_connected')
        pass
    
    def tryConnection(self,button, connectionType, currStateLabel):
            ###TODO: Define connect function with api###
            import random
            self.app= MDApp.get_running_app()
            randInt = random.randint(0,1)
            if self.ids.rfc_button.disabled == False:
                print("RFC")
            elif self.ids.lte_button.disabled == False:
                lteAddress=self.ids.lte_address
                print("LTE adress:"+str(lteAddress.text))
            if randInt == 0:
                currStateLabel.text = self.app.root.ids.translator.translate('failed_message')
                currStateLabel.color = self.app.customColors["failure"]
            else:
                button.disabled = True
                currStateLabel.text = self.app.root.ids.translator.translate('success_message')
                currStateLabel.color = self.app.customColors["success"]
                print(self.ids.vehicle_item.current_item)
                """
                drone = ArduPlaneObject("name", "uuid", "model", "VTOl", "udp",
                                        "udpin:192.168.1.58:14550", None)
                self.app.set_drone_instance(drone)
                self.app.drone.connect()
                self.app.drone.arm()
                self.app.drone.takeoff()
                """
                self.app.connected = True
                Clock.schedule_once(partial(self.app.changeScreen, 'main'), 3)
                print("OK")