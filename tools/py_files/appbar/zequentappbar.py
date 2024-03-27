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
from zequentmavlinklib.ArduPlane import ArduPlaneObject, MavResult, list_all_commands

from tools.py_files.widgets.zequentmapview import ZequentMapView
from tools.py_files.widgets.zequenttoast import ZequentToast
import logging
from logging import getLogger

log = getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ZequentAppBar(MDTopAppBar):
    translator = None

    submitDialog = None
    languageDropdown = None

    mavResult: MavResult = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drone = None
        self.app = None

    def build(self):
        pass

    def open_language_dropdown(self, item):
        self.languageDropdown = ZequentDropDownMenu(caller=item, items=self.get_language_drop_down_items())
        self.languageDropdown.pos_hint = {'center_x': .5, 'center_y': .5}
        self.languageDropdown.open()

    def get_language_drop_down_items(self):
        self.app = MDApp.get_running_app()
        from os import walk

        available_languages = []
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
            available_languages.append(currLanguageDropDownItem)

        return available_languages

    def show_alert_dialog(self, language):
        self.translator = self.app.root.ids.translator
        cancel_button = ZequentFlatButton()
        cancel_button.text = self.translator.translate("cancel")
        cancel_button.bind(on_press=self.hide_alert_dialog)
        submit_button = ZequentFlatButton()
        submit_button.text = self.translator.translate("submit")
        submit_button.bind(on_press=partial(self.set_language, language))
        self.submitDialog = ZequentDialog(
            buttons=[
                cancel_button,
                submit_button
            ]
        )
        self.submitDialog.text = self.translator.translate('restart_text')
        self.submitDialog.open()

    def set_language(self, *args):
        self.translator.set_locale(args[0])
        self.save_in_settings(args[0])

    def save_in_settings(self, language):
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
        self.app = MDApp.get_running_app()
        self.specialCommandsDropdown = ZequentDropDownMenu(caller=item, items=self.get_special_commands_drop_down_items())
        self.specialCommandsDropdown.pos_hint = {'right': 1, 'top': 1}
        self.specialCommandsDropdown.open()

    # TODO sabri! Commands in List

    def get_special_commands_drop_down_items(self):
        self.app = MDApp.get_running_app()
        self.drone: ArduPlaneObject = self.app.drone
        available_special_commands = []

        action_object_list = self.drone.get_basic_commands()

        for action in action_object_list:
            curr_special_command_drop_down_item = {
                "text": action.key,
                "font_size": self.app.fontSizes['primary'],
                "on_release": lambda command=action.command: self.execute_special_command(command),
            }
            available_special_commands.append(curr_special_command_drop_down_item)
        return available_special_commands

    def execute_special_command(self, method):
        self.execute_special_command_worker(method)
        if hasattr(self.mavResult, 'details'):
            # log.info(self.mavResult.details)
            ZequentToast.showInfoMessage(self.mavResult.details)

    def execute_special_command_worker(self, method, *args):
        command = getattr(ArduPlaneObject, method)
        if args is not None:
            self.mavResult = command(self.drone, *args)
            print(self.mavResult)
        else:
            self.mavResult = command(self.drone)
            print(self.mavResult)
