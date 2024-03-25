from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.py_files.layouts.casuals.zequentanchorlayout import *
from tools.py_files.layouts.casuals.zequentgridlayout import *
from kivy.clock import Clock
from functools import partial
from kivymd.app import MDApp
from tools.Utils import *
from tools.py_files.widgets.zequentdropdownitem import ZequentDropDownItem
from tools.py_files.widgets.zequenttoast import *
from zequentmavlinklib.ArduPlane import ArduPlaneObject
from zequentmavlinklib.Globals import ConnectionType, ErrorMessage, WorkerThread
from pymavlink.dialects.v20.common import MAVLink_heartbeat_message
from logging import getLogger


log = getLogger(__name__)
logging.basicConfig(level=logging.INFO)  

class ZequentConnectionLayout(ZequentGridLayout):
    connectionStatusText = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        if self.app.root is not None:
            self.connectionStatusText = self.app.root.ids.translator.translate('not_connected')
         
    
    def build(self):
        pass

    def execute_connect(self):
        return self.drone.connect()
    
    def tryConnection(self,button, connectionType, currStateLabel):
            self.app= MDApp.get_running_app()
            if self.ids.rfc_button.disabled == False:
                self.app.log.info("RFC")
            elif self.ids.lte_button.disabled == False:
                lteAddress=self.ids.lte_address
                lteAddress=str(lteAddress.text)
                if lteAddress is None or lteAddress is "":
                    ZequentToast.showInfoMessage(self.app.root.ids.translator.translate('lte_address_input_invalid'))
                    return 
                else:
                    log.info("LTE adress:"+ lteAddress)
                    connectionType: ZequentDropDownItem = self.ids.lte_connection_type 
                    log.info(connectionType.current_item)

                    log.info(lteAddress)

                self.drone = ArduPlaneObject("TestVtol","testuuid", "OrgId", "TestModel", ConnectionType.UDPIN, "127.0.0.1",
                                        "14550", None)
                connectThread = self.drone.connect()
                print("---------------------------------------------------------")
                print(connectThread)

            if isinstance(connectThread.response, ErrorMessage) or connectThread.response is None:
                connectThread.response : ErrorMessage
                currStateLabel.text = self.app.root.ids.translator.translate('failed_message')
                currStateLabel.color = self.app.customColors["failure"]
                ZequentToast.showErrorMessage(connectThread.response.message)
            else:
                connectThread.response: MAVLink_heartbeat_message
                self.app.set_drone_instance(self.drone)
                button.disabled = True
                currStateLabel.text = self.app.root.ids.translator.translate('success_message')
                currStateLabel.color = self.app.customColors["success"]
                self.app.set_vehicle_type(str(self.ids.vehicle_item.current_item))
                Clock.schedule_once(partial(self.app.changeScreen, 'main'), 3)
                log.info("OK")