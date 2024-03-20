import random
import threading
from kivymd.uix.toolbar.toolbar import MDTopAppBar
import json
from tools.Utils import *
from kivymd.app import MDApp
from tools.py_files.screenmanager.zequentrootscreenmanager import ZequentRootScreenManager
from tools.py_files.widgets.zequentdropdownmenu import *
from tools.py_files.widgets.zequentdialog import *
from tools.py_files.widgets.zequentflatbutton import *
from tools.py_files.widgets.zequentbutton import *
from functools import partial
from zequentmavlinklib.ArduPlane import ArduPlaneObject, MavResult


from tools.py_files.widgets.zequentmapview import ZequentMapView
from tools.py_files.widgets.zequenttoast import ZequentToast


class ZequentAppBar(MDTopAppBar):

    translator = None
  
    submitDialog = None
    languageDropdown = None

    mavResult: MavResult = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        pass
    
    def open_language_dropdown(self, item):
        self.languageDropdown = ZequentDropDownMenu(caller=item, items=self.getLanguageDropDownItems())
        self.languageDropdown.pos_hint = {'center_x':.5,'center_y':.5}
        self.languageDropdown.open()

    def getLanguageDropDownItems(self):
        self.app= MDApp.get_running_app()
        from os import walk

        availableLanguages = []
        for (dirpath, dirnames, filenames) in walk(Utils.getTranslatorFolder()):
            filenames = filenames
            break

        for filename in filenames:
            filename = filename.split('.json')[0]
            currLanguageDropDownItem = {
                "text": filename,
                "font_size": self.app.fontSizes['primary'],
                "on_release": lambda language=filename: self.show_alert_dialog(language),
            }
            availableLanguages.append(currLanguageDropDownItem)
        
        return availableLanguages
    
    def show_alert_dialog(self, language):
        self.translator = self.app.root.ids.translator
        cancelButton = ZequentFlatButton()
        cancelButton.text = self.translator.translate("cancel")
        cancelButton.bind(on_press=self.hide_alert_dialog) 
        submitButton = ZequentFlatButton()
        submitButton.text=self.translator.translate("submit")
        submitButton.bind(on_press=partial(self.setLanguage,language))
        self.submitDialog = ZequentDialog(
                buttons=[
                    cancelButton,
                    submitButton
                ]
            )
        self.submitDialog.text = self.translator.translate('restart_text')
        self.submitDialog.open()

    def setLanguage(self, *args):
        self.translator.set_locale(args[0])
        self.saveInSettings(args[0])
    

    def saveInSettings(self, language):
        with open(Utils.getSettingsFile()) as infile:
            data = json.load(infile)
        data["lastUsedLanguage"] = language
        with open(Utils.getSettingsFile(), 'w') as outfile:
            json.dump(data, outfile)
            self.app.stop()

    def hide_alert_dialog(self, instance):
        self.languageDropdown.dismiss()
        self.submitDialog.dismiss()

    def open_special_commands(self, item):
        self.app= MDApp.get_running_app()
        self.specialCommandsDropdown = ZequentDropDownMenu(caller=item, items=self.getSpecialCommandsDropDownItems())
        self.specialCommandsDropdown.pos_hint = {'right':1,'top':1}
        self.specialCommandsDropdown.open()


    #TODO sabri! Commands in List

    def getSpecialCommandsDropDownItems(self):
        self.app=MDApp.get_running_app()
        self.drone: ArduPlaneObject = self.app.drone
        availableSpecialCommands = []
        currSpecialCommandDropDownItem = {
            "text": 'Arm Vehicle',
            "font_size": self.app.fontSizes['primary'],
            "on_release": lambda command='Arm Vehicle': self.execute_special_command(self.drone.arm),
        }
        currSpecialCommandDropDownItem2 = {
            "text": 'Take-Off (Default)',
            "font_size": self.app.fontSizes['primary'],
            "on_release": lambda command='Takeoff': self.execute_special_command(self.drone.takeoff),
        }
        availableSpecialCommands.append(currSpecialCommandDropDownItem)
        availableSpecialCommands.append(currSpecialCommandDropDownItem2)
        return availableSpecialCommands
        
        
    def test(self,command):
        sm: ZequentRootScreenManager = self.app.root.ids.sm
        mapview: ZequentMapView = sm.current_screen.ids.main_controller_layout.ids.camera_layout.ids.mapview
        randInt = random.uniform(0,.0000200)
    
        print(mapview.change_pos_marker(0.0000008,randInt))

    def execute_special_command(self, method):
        thread = threading.Thread(target= lambda: self.execute_special_command_worker(method))
        thread.start()
        thread.join()
        print("Command Execuiton finished")
        if hasattr(self.mavResult, 'details'):
            print(self.mavResult.details)
            ZequentToast().zequentToast(self.mavResult.details)
       


    def execute_special_command_worker(self, method):
        self.mavResult =  method()
