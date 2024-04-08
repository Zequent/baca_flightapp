from PyQt5.QtWidgets import *
from PyQt5 import uic
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class ConnectionLayout(QMainWindow):
    def __init__(self):
        super(ConnectionLayout, self).__init__()
        self.combo_box = None
        uic.loadUi("./ui-layouts/connectionlayout.ui", self)
        self.show()
        self.combo_box: QComboBox = self.connection_type_selector
        self.combo_box.currentIndexChanged.connect(self.connection_type_changed)

        toolbar = self.toolBar
        toolbar.addAction('takeoff', QPushButton)
        toolbar.addAction('land_now', QPushButton)
        toolbar.addAction('return_to_launch', QPushButton)

        toolbar.setEnabled(False)

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
