from tools.py_files.core.graphicalchangeexecutor import GraphicalChangeExecutor
from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.py_files.layouts.casuals.zequentanchorlayout import *
from tools.py_files.layouts.casuals.zequentgridlayout import *
from kivy.clock import Clock
from functools import partial
from kivymd.app import MDApp
from tools.Utils import *

from tools.py_files.widgets.zequentbutton import ZequentButton
from tools.py_files.widgets.zequentdropdownitem import ZequentDropDownItem
from tools.py_files.widgets.zequentlabel import ZequentLabel
from tools.py_files.widgets.zequentspinner import ZequentSpinner
from tools.py_files.widgets.zequenttoast import *
from zequentmavlinklib.ArduPlane import ArduPlaneObject
from zequentmavlinklib.Globals import ConnectionType, ErrorMessage, WorkerThread
from pymavlink.dialects.v20.common import MAVLink_heartbeat_message
from logging import getLogger
from kivy.clock import mainthread
import weakref

log = getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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

    def tryConnection(self, *args):

        button: ZequentButton = self.ids.connect_button
        connectionType: ZequentGridLayout = self.ids.connection_type
        currStateLabel: ZequentLabel = self.ids.connection_status_label

        self.app = MDApp.get_running_app()
        if self.ids.rfc_button.disabled == False:
            self.app.log.info("RFC")
        elif self.ids.lte_button.disabled == False:
            lteAddress = self.ids.lte_address
            lteAddress = str(lteAddress.text)
            if lteAddress is None or lteAddress is "":
                ZequentToast.showInfoMessage(self.app.root.ids.translator.translate('lte_address_input_invalid'))
                return
            else:
                # log.info("LTE adress:"+ lteAddress)
                connectionType: ZequentDropDownItem = self.ids.lte_connection_type
                # log.info(connectionType.current_item)
                # log.info(lteAddress)
                self.drone = ArduPlaneObject("TestVtol", "testuuid", "OrgId", "TestModel",
                                             ConnectionType.UDPIN, "192.168.1.25", "14550", None)
                connectionResponse = self.drone.connect()

        if isinstance(connectionResponse, ErrorMessage):
            GraphicalChangeExecutor.execute(self.remove_spinner)
            connectionResponse: ErrorMessage
            currStateLabel.text = self.app.root.ids.translator.translate('failed_message')
            currStateLabel.color = self.app.customColors["failure"]
            ZequentToast.showErrorMessage(connectionResponse.message)
            GraphicalChangeExecutor.execute(self.enable_widgets)
        else:
            connectionResponse: MAVLink_heartbeat_message
            self.app.set_drone_instance(self.drone)
            button.disabled = True
            currStateLabel.text = self.app.root.ids.translator.translate('success_message')
            currStateLabel.color = self.app.customColors["success"]
            self.app.set_vehicle_type(str(self.ids.vehicle_item.current_item))
            Clock.schedule_once(partial(self.app.changeScreen, 'main'), 3)

    def add_spinner(self, button):
        connection_grid: ZequentGridLayout = self.ids.connection_grid
        anchorLayout = ZequentAnchorLayout()
        spinner = ZequentSpinner()
        spinner.opacity = 1
        anchorLayout.add_widget(spinner)
        connection_grid.add_widget(anchorLayout)
        self.ids['anchor_layout_spinner'] = weakref.ref(anchorLayout)
        self.disable_widgets()

        thread = WorkerThread(method=self.tryConnection, name="Connecting to Vehicle")
        thread.start()
        thread.join()

    def remove_spinner(self):
        self.ids.connection_grid.remove_widget(self.ids.anchor_layout_spinner)

    def disable_widgets(self):
        self.ids.vehicle_item.opacity = 0
        self.ids.connection_type.opacity = 0
        self.ids.connection_grid.disabled = True

    def enable_widgets(self):
        self.ids.vehicle_item.opacity = 1
        self.ids.connection_type.opacity = 1
        self.ids.connection_grid.disabled = False
