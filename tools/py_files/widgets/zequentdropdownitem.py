from kivymd.uix.dropdownitem.dropdownitem import MDDropDownItem
from zequentmavlinklib.Globals import VehicleTypes
from zequentmavlinklib.Globals import ConnectionType
from tools.py_files.widgets.zequentdropdownmenu import *
from kivymd.app import MDApp

class ZequentDropDownItem(MDDropDownItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
    
    def build(self):
        pass


    ##VEHICLES
    def getInitialVehicle(self):
        return str(VehicleTypes(1).name)

    def openVehicleMenu(self,item):
        self.vehicleTypeDropDown = ZequentDropDownMenu(caller=item, items=self.getVehicleTypesItems())
        self.vehicleTypeDropDown.open()
        
    def getVehicleTypesItems(self):
        availableTypes = []
        for vehicle in VehicleTypes:
            currVehicleDropDownItem = {
                "text": vehicle.name,
                "font_size": self.app.fontSizes['primary'],
                "on_release": lambda vehicleType=vehicle.name: self.setVehicle(vehicleType),
            }
            availableTypes.append(currVehicleDropDownItem)
        return availableTypes
    
    def setVehicle(self, vehicleType):
        self.set_item(vehicleType)
        self.app.vehicleType = vehicleType
        self.vehicleTypeDropDown.dismiss()

    ##LTE CONNECITON TYPE
    def getInitialConnectionType(self):
        return str(ConnectionType('udpin:').name)
    
    def openLTEConnectionTypeMenu(self,item):
        self.lteConnectionTypeDropDown = ZequentDropDownMenu(caller=item, items=self.getLTEConnectionTypesItems())
        self.lteConnectionTypeDropDown.open()

    def getLTEConnectionTypesItems(self):
        availableTypes = []
        for connectionType in ConnectionType:
            currLTEConnectionTypeDropDownItem = {
                "text": connectionType.name,
                "font_size": self.app.fontSizes['primary'],
                "on_release": lambda connectionType=connectionType.name: self.setLTEConnectionType(connectionType),
            }
            availableTypes.append(currLTEConnectionTypeDropDownItem)
        return availableTypes
    
    def setLTEConnectionType(self, connectionType):
        self.set_item(connectionType)
        self.app.connectionType = connectionType
        self.lteConnectionTypeDropDown.dismiss()