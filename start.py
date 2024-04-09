from PyQt5.QtCore import pyqtSignal, QThread, QTimer, QObject
from PyQt5.QtWidgets import *
from PyQt5 import uic
import logging

from zequentmavlinklib.ArduPlane import ArduPlaneObject, ConnectionType

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class PositionReceiver(QObject):
    position_received = pyqtSignal(object)  # Signal to indicate the reception of a position object

    def __init__(self, drone):
        super().__init__()

        # Start a timer to simulate receiving position objects (replace this with your actual data reception mechanism)
        self.drone = drone
        self.timer = QTimer()
        self.timer.timeout.connect(self.receive_position)
        self.timer.start(500)  # Receive position every 1 second


    def receive_position(self):
        # Simulated position object
        position = self.drone.get_position()  # Replace this with your actual position data

        # Emit the position_received signal with the received position object
        self.position_received.emit(position)

class ConnectionLayout(QMainWindow):
    drone = 4
    def __init__(self):
        super(ConnectionLayout, self).__init__()
        self.combo_box = None
        uic.loadUi("./ui-layouts/connectionlayout.ui", self)
        self.show()
        self.combo_box: QComboBox = self.connection_type_selector
        self.combo_box.currentIndexChanged.connect(self.connection_type_changed)
        self.drone = ArduPlaneObject("TestVtol", "testuuid", "OrgId", "TestModel",
                                     ConnectionType.UDPIN, "192.168.1.25", "14540", None)

        self.drone.connect()


        takeOffBut = QAction("TAKEOFF", self)
        takeOffBut.triggered.connect(lambda: self.action_executor(func=self.drone.takeoff))

        armButt = QAction("ARMING", self)
        armButt.triggered.connect(lambda:self.action_executor(func=self.drone.arm))

        get_pos_action = QAction("GET_POSITION", self)
        get_pos_action.triggered.connect(lambda: self.action_executor(func=self.drone.get_position))

        toolbar = self.toolBar
        toolbar.addAction(takeOffBut)
        toolbar.addAction(armButt)
        toolbar.addAction(get_pos_action)
        self.testlabel = QLabel()
        self.testlabel.setText("INIT")
        layout = QVBoxLayout()
        layout.addWidget(self.testlabel)


        self.centralWidget().setLayout(layout)



        self.position_receiver = PositionReceiver(self.drone)
        self.position_receiver.position_received.connect(self.handle_position_received)

    def handle_position_received(self, position):
        print("Received position:", position)
        self.testlabel.setText(str(position))
        # Process the received position here




    def execute_worker_command(self):
        # Create a new worker thread and start it only if the previous one has completed
        res = self.drone.get_position()

    def action_executor(self, func, *args, **kwargs):
       res = func()
       self.handle_result(res)

    def handle_result(self, result):
        self.result = result
        print(self.result)

    def show_message_box(self):
        msg_box = QLabel()
        msg_box.setText(self.result)

    def takeoff(self):
        pass


    def connection_type_changed(self):
        print(self.combo_box.currentText())
        if self.combo_box.currentText() == 'RFC':
            self.ipaddress_input.setEnabled(False)
        elif self.combo_box.currentText() == 'LTE':
            self.ipaddress_input.setEnabled(True)


def main():
    log.info("Starting Application")
    log.error("test")
    app = QApplication([])
    window = ConnectionLayout()
    app.exec()


if __name__ == '__main__':
    main()
