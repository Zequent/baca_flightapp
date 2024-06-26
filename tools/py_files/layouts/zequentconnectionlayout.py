from tools.py_files.core.graphicalchangeexecutor import GraphicalChangeExecutor
from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.py_files.layouts.casuals.zequentanchorlayout import *
from tools.py_files.layouts.casuals.zequentgridlayout import *
from kivy.clock import Clock
from functools import partial
from kivymd.app import MDApp
from tools.Utils import *

from tools.py_files.widgets.expansionpanel.zequentexpansionpanel import ZequentExpansionPanel
from tools.py_files.widgets.zequentbutton import ZequentButton
from tools.py_files.widgets.zequentdropdownitem import ZequentDropDownItem
from tools.py_files.widgets.zequentlabel import ZequentLabel
from tools.py_files.widgets.zequentspinner import ZequentSpinner
from tools.py_files.widgets.zequenttoast import *
from zequentmavlinklib.ArduPlane import ArduPlaneObject
from zequentmavlinklib.Globals import ConnectionType, ErrorMessage
from pymavlink.dialects.v20.common import MAVLink_heartbeat_message
from logging import getLogger
import weakref
import weakref
import concurrent.futures
from kivy.properties import NumericProperty

log = getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ZequentConnectionLayout(GridLayout):
    connectionStatusText = ''

    cols= NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drone = None
        self.app = MDApp.get_running_app()
        self.spinner = None
        if self.app.root is not None:
            self.connectionStatusText = self.app.translator.translate('not_connected')
        

    def build(self):
        pass

    def execute_connect(self):
        return self.drone.connect()

    def try_connection(self, *args):

        button: ZequentButton = self.ids.connect_button
        currConnectionType: ZequentDropDownItem = self.ids.connection_type_dropdown
        curr_state_label: ZequentLabel = self.ids.connection_status_label
        self.app = MDApp.get_running_app()

        if currConnectionType.current_item == "RFC":
            self.app.log.info("RFC")
        else:
            lte_address = self.ids.lte_address
            lte_address = str(lte_address.text)
            if lte_address is None or lte_address is "":
                ZequentToast.showInfoMessage(self.app.translator.translate('lte_address_input_invalid'))
                return
            else:
                # log.info("LTE adress:"+ lte_address)
                # log.info(connectionType.current_item)
                # log.info(lte_address)
                tmp_connectionType = None
                if currConnectionType.current_item == "UDPIN":
                    tmp_connectionType=ConnectionType.UDPIN
                elif currConnectionType.current_item == "TCPIN":
                    tmp_connectionType=ConnectionType.TCPIN

                self.drone = ArduPlaneObject("TestVtol", "testuuid", "OrgId", "TestModel",
                                             tmp_connectionType, lte_address, "14550", None)
                connection_response = execute_with_thread(name="Connecting to Drone", method=self.drone.connect)
                self.on_thread_complete(connection_response)

        if not isinstance(connection_response, ErrorMessage):
            connection_response: MAVLink_heartbeat_message
            self.app.set_drone_instance(self.drone)
            button.disabled = True
            curr_state_label.text = self.app.translator.translate('success_message')
            curr_state_label.color = self.app.customColors["success"]
            self.app.set_vehicle_type(str(self.ids.vehicle_item.current_item))
            Clock.schedule_once(partial(self.app.changeScreen, 'main'), 3)
        else:
            GraphicalChangeExecutor.execute(self.remove_spinner)
            connection_response
            curr_state_label.text = self.app.translator.translate('failed_message')
            curr_state_label.color = self.app.customColors["failure"]
            ZequentToast.showErrorMessage(connection_response.message)
            GraphicalChangeExecutor.execute(self.enable_widgets)
      


    def add_spinner(self):
        self.spinner = ZequentSpinner()
        self.anchor_layout.add_widget(self.spinner)   
        self.connection_grid.add_widget(self.anchor_layout)
    
    def start_connecting_process(self, button):
        self.connection_grid: ZequentGridLayout = self.ids.connection_type_layout
        self.anchor_layout = ZequentAnchorLayout()
        self.ids['anchor_layout_spinner'] = weakref.ref(self.anchor_layout)
        
        GraphicalChangeExecutor.execute(self.add_spinner)

        self.disable_widgets()
        execute_with_thread(method=self.try_connection, name="Connecting to Vehicle")

    
    def on_thread_complete(self, res):
        #self.spinner.opacity = 1
        if res is not None:
            GraphicalChangeExecutor.execute(self.enable_widgets)
            pass


    
    def remove_spinner(self):
        self.ids.connection_type_layout.remove_widget(self.ids.anchor_layout_spinner)


    
    def disable_widgets(self):
        self.ids.vehicle_item.opacity = 0
        self.ids.connection_type_layout.opacity = 0
       # self.ids.connection_grid.disabled = True

    def enable_widgets(self):
        self.ids.vehicle_item.opacity = 1
        self.ids.connection_type_layout.opacity = 1
        #self.ids.connection_grid.disabled = False