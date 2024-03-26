from tools.py_files.layouts.casuals.zequentboxlayout import ZequentBoxLayout
from tools.py_files.layouts.casuals.zequentgridlayout import ZequentGridLayout
from tools.py_files.layouts.casuals.zequentstacklayout import ZequentStackLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import mainthread
from tools.py_files.widgets.zequentlabel import ZequentLabel
from kivymd.app import MDApp

class ZequentLogs(ZequentBoxLayout):
    logs=StringProperty()
    fixedValues=ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.cols=1
        self.orientation='vertical'
        self.app= MDApp.get_running_app()
    
    def build(self):
        pass

    @mainthread
    def on_logs(self, *args):
        newLog = ZequentLabel(text=self.logs)
        newLog.font_size = self.app.fontSizes["tertiary"]
        newLog.text_size = self.width,None

        if len(self.children) < 5:
            self.add_widget(newLog)
        elif len(self.children) >= 5:
            self.remove_widget(self.children[len(self.children)-1])

    @mainthread
    def on_fixedValues(self, *args):
        for value in self.fixedValues:
            newLog = ZequentLabel(text=value)
            newLog.font_size = self.app.fontSizes["tertiary"]
            newLog.text_size = self.width,None
            self.add_widget(newLog)


