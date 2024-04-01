from tools.py_files.layouts.casuals.zequentboxlayout import ZequentBoxLayout
from tools.py_files.layouts.casuals.zequentgridlayout import ZequentGridLayout
from tools.py_files.layouts.casuals.zequentstacklayout import ZequentStackLayout
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.clock import mainthread
from tools.py_files.widgets.zequentlabel import ZequentLabel
from kivymd.app import MDApp
from zequentmavlinklib.ArduPlane import ArduPlaneObject

class ZequentLogs(ZequentBoxLayout):
    #logs=StringProperty()
    drone=ObjectProperty()
    isArmed = StringProperty("Default")
    battery = StringProperty("Default")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.cols=1
        self.orientation='vertical'
        self.app= MDApp.get_running_app()
        self.drone: ArduPlaneObject = self.app.drone
        self.armWidget = ZequentLabel(text=self.isArmed)
        self.batteryWidget = ZequentLabel(text=self.battery)
        self.add_widget(self.armWidget)
        self.add_widget(self.batteryWidget)
    
    def build(self):
        pass

    @mainthread
    def on_isArmed(self, instance, *args):
        self.isArmed = str(self.drone.is_armed)
        print("---------------------------")
        print(self.isArmed)
        self.armWidget.text = self.isArmed
        #arm_state = ZequentLabel(text=str(self.drone.is_armed))

    @mainthread
    def on_battery(self,instance,  *args):
        self.battery = str(self.drone.battery)
        self.batteryWidget.text = self.battery
        #battery_status = ZequentLabel(text=str(self.drone.battery))


'''   @mainthread
    def on_logs(self, *args):
        newLog = ZequentLabel(text=self.logs)
        newLog.font_size = self.app.fontSizes["tertiary"]
        newLog.text_size = self.width,None

        if len(self.children) < 5:
            self.add_widget(newLog)
        elif len(self.children) >= 5:
            self.remove_widget(self.children[len(self.children)-1])
'''


