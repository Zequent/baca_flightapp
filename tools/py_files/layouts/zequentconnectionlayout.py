from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.py_files.layouts.casuals.zequentanchorlayout import *
from tools.py_files.layouts.casuals.zequentgridlayout import *
from kivy.clock import Clock
from functools import partial
from kivymd.app import MDApp
from tools.Utils import *
from tools.py_files.widgets.zequentdropdownitem import ZequentDropDownItem
from tools.py_files.widgets.zequenttoast import *
from zequentmavlinklib.ArduPlane import ArduPlaneObject, ConnectionType



class ZequentConnectionLayout(ZequentGridLayout):
    
    connectionStatusText = ''


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        if self.app.root is not None:
            self.connectionStatusText = self.app.root.ids.translator.translate('not_connected')
         
    
    def build(self):
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
                lteAddress=str(lteAddress.text)
                if lteAddress is None or lteAddress is "":
                    ZequentToast.showInfoMessage(self.app.root.ids.translator.translate('lte_address_input_invalid'))
                    return 
                else:
                    print("LTE adress:"+ lteAddress)
                    connectionType: ZequentDropDownItem = self.ids.lte_connection_type 
                    print(connectionType.current_item)

                    print(lteAddress)

            #TODO hier noch ein check einbauen - richtig Connected oder nicht (Simulator bei @Mina aufsetzen!!)
            if randInt == 0:
                currStateLabel.text = self.app.root.ids.translator.translate('failed_message')
                currStateLabel.color = self.app.customColors["failure"]
            else:
                button.disabled = True
                currStateLabel.text = self.app.root.ids.translator.translate('success_message')
                currStateLabel.color = self.app.customColors["success"]
                
                print(connectionType)

                drone = ArduPlaneObject("TestVtol","testuuid", "OrgId", "TestModel", ConnectionType.UDPIN, "127.0.0.1",
                                        "14550", None)
                self.app.set_drone_instance(drone)
                try:
                    self.app.drone.connect()
                except TimeoutError as error :
                    message = self.app.root.ids.translator.translate(error)
                    ZequentToast.showInfoMessage(message)
                
                

                self.app.set_vehicle_type(str(self.ids.vehicle_item.current_item))
                
                Clock.schedule_once(partial(self.app.changeScreen, 'main'), 3)
                print("OK")