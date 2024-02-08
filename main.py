import tools.i18n as i18n
from kivymd.app import MDApp
from kivy.properties import BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from functools import partial

translator = i18n.Translator('tools/localization/')
translator.set_locale('de')

class MainControllerLayout(MDBoxLayout):
    pass


class ZequentMavLinkApp(MDApp):
    toolBarTitle = "MavLink"
    connected = False
    isMainLayoutShown = BooleanProperty(False)

    colors = {
        "Black-primary": [0,0,0,0.9],
        "Gold-primary": [0.78,0.56,0.05,1],
        "Gold-secondary": [0.78,0.56,0.05,0.5],
        "Jewel-primary": [0.00392, 0.14117, 0.3607],
        "Success": [0,1,0,1],
        "Failure": [1,0,0,1],
    }
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
    def get_welcome_text(self):
        return translator.translate('welcome')
    def callback(self,x):
        print(x)

    ######ZequentConnectLayout#######
    def getConnectionStatusText(self):
        return translator.translate('not_connected')
    
    def setNewScreen(self,*args):
        self.root.clear_widgets()
        self.root.add_widget(args[0])

    def tryConnection(self,button, connectionType):
        import random
        randInt = random.randint(0,1)
        currStateLabel = self.root.ids.connection_status_label
        
        if connectionType.ids.rfc_button.disabled == False:
            print("RFC")
        elif connectionType.ids.lte_button.disabled == False:
            address=connectionType.ids.lte_address
            print("LTE adress:"+str(address.text))

            

        if randInt is 0:
            currStateLabel.text = translator.translate('failed_message')
            currStateLabel.color = self.colors["Failure"]
        else:
            button.disabled = True
            currStateLabel.text = translator.translate('success_message')
            currStateLabel.color = self.colors["Success"]
            Clock.schedule_once(partial(self.setNewScreen, MainControllerLayout()), 3)

if __name__ == '__main__':
    ZequentMavLinkApp().run()