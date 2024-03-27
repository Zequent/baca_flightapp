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
        self.drone = None
        self.app = MDApp.get_running_app()
        if self.app.root is not None:
            self.connectionStatusText = self.app.root.ids.translator.translate('not_connected')

    def build(self):
        pass

    def execute_connect(self):
        return self.drone.connect()

    def try_connection(self, *args):

        button: ZequentButton = self.ids.connect_button
        connectionType: ZequentGridLayout = self.ids.connection_type
        curr_state_label: ZequentLabel = self.ids.connection_status_label

        self.app = MDApp.get_running_app()
        if not self.ids.rfc_button.disabled:
            self.app.log.info("RFC")
        elif not self.ids.lte_button.disabled:
            lte_address = self.ids.lte_address
            lte_address = str(lte_address.text)
            if lte_address is None or lte_address is "":
                ZequentToast.showInfoMessage(self.app.root.ids.translator.translate('lte_address_input_invalid'))
                return
            else:
                # log.info("LTE adress:"+ lte_address)
                connectionType: ZequentDropDownItem = self.ids.lte_connection_type
                # log.info(connectionType.current_item)
                # log.info(lte_address)
                self.drone = ArduPlaneObject("TestVtol", "testuuid", "OrgId", "TestModel",
                                             ConnectionType.UDPIN, lte_address, "14550", None)
                connection_response = self.drone.connect()

        if isinstance(connection_response, ErrorMessage):
            GraphicalChangeExecutor.execute(self.remove_spinner)
            connection_response: ErrorMessage
            curr_state_label.text = self.app.root.ids.translator.translate('failed_message')
            curr_state_label.color = self.app.customColors["failure"]
            ZequentToast.showErrorMessage(connection_response.message)
            GraphicalChangeExecutor.execute(self.enable_widgets)
        else:
            connection_response: MAVLink_heartbeat_message
            self.app.set_drone_instance(self.drone)
            button.disabled = True
            curr_state_label.text = self.app.root.ids.translator.translate('success_message')
            curr_state_label.color = self.app.customColors["success"]
            self.app.set_vehicle_type(str(self.ids.vehicle_item.current_item))
            Clock.schedule_once(partial(self.app.changeScreen, 'main'), 3)

    def start_connecting_process(self, button):
        connection_grid: ZequentGridLayout = self.ids.connection_grid
        anchor_layout = ZequentAnchorLayout()
        spinner = ZequentSpinner()
        spinner.opacity = 1
        anchor_layout.add_widget(spinner)
        connection_grid.add_widget(anchor_layout)
        self.ids['anchor_layout_spinner'] = weakref.ref(anchor_layout)
        self.disable_widgets()

        thread = WorkerThread(method=self.try_connection, name="Connecting to Vehicle")
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