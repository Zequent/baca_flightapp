from kivymd.uix.toolbar.toolbar import MDTopAppBar
import json
from tools.Utils import *
from kivymd.app import MDApp
from tools.py_files.widgets.zequentdropdownmenu import *
from tools.py_files.widgets.zequentdialog import *
from tools.py_files.widgets.zequentflatbutton import *
from tools.py_files.widgets.zequentbutton import *
from functools import partial


class ZequentAppBar(MDTopAppBar):

    translator = None
    app=MDApp.get_running_app()
    submitDialog = None
    languageDropdown = None

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
        