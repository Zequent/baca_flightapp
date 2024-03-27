from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from tools.Utils import *
from kivymd.app import MDApp



class ZequentNavigationDrawer(MDNavigationDrawer):
    isCreated = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def on_state(self, widget, state):
        if not self.isCreated:
            self.app=MDApp.get_running_app()
            navigationItems = Utils.getNavigationDrawerItems(self.app.translator, self.app.root.ids.sm)
            
            for item in navigationItems:
                self.ids.drawer_menu.add_widget(item)
            self.isCreated=True
            
                