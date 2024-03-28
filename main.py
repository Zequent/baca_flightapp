from kivymd.app import MDApp
from kivy.clock import Clock
from functools import partial
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
import os

import weakref
##toast
from kivymd.toast import toast
##Permission
from kivy import platform
from plyer import gps
from tools.android.permissions import AndroidPermissions

##APPBAR
from tools.py_files.appbar.zequentappbar import *

##LAYOUTS
from tools.py_files.layouts.maincontrollerlayout import *
from tools.py_files.layouts.zequentcameralayout import *
from tools.py_files.layouts.zequentconnectionlayout import *
from tools.py_files.layouts.zequentlogs import *
from tools.py_files.layouts.zequentrootlayout import *

##Layouts-CASUALS
from tools.py_files.layouts.casuals.zequentanchorlayout import *
from tools.py_files.layouts.casuals.zequentboxlayout import *
from tools.py_files.layouts.casuals.zequentfloatlayout import *
from tools.py_files.layouts.casuals.zequentgridlayout import *
from tools.py_files.layouts.casuals.zequentpagelayout import *
from tools.py_files.layouts.casuals.zequentrelativelayout import *
from tools.py_files.layouts.casuals.zequentscatterlayout import *
from tools.py_files.layouts.casuals.zequentstacklayout import *

##Navigationdrawer
from tools.py_files.navigationdrawer.zequentnavigationdrawer import *


##SCREENMANAGER
from tools.py_files.screenmanager.zequentrootscreenmanager import *


##Translator
from tools.py_files.translator.translator import *

##WIDGETS
from tools.py_files.widgets.expansionpanel.zequentexpansionpanel import *
from tools.py_files.widgets.zequentactionicon import *
from tools.py_files.widgets.zequentbutton import *
from tools.py_files.widgets.zequentconnectionbutton import *
from tools.py_files.widgets.zequentdialog import *
from tools.py_files.widgets.zequentdropdownitem import *
from tools.py_files.widgets.zequentdropdownmenu import *
from tools.py_files.widgets.zequentflatbutton import *
from tools.py_files.widgets.zequentlabel import *
from tools.py_files.widgets.zequentmapview import *
from tools.py_files.widgets.zequentsingletextinput import *
from tools.py_files.widgets.zequentspinner import *
from tools.py_files.widgets.zequenttoast import *

###IMPORT ALL KV_FILES
def importKV_FILES():
    for currDirName, dirnames, filenames in os.walk('./tools/kv_files'):
        for filename in filenames:
            if not currDirName.__contains__("screens"):
                Builder.load_file(os.path.join(currDirName, filename)) 

log = getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
class ZequentMavLinkApp(MDApp):

    latitude = NumericProperty(48)
    longitude = NumericProperty(48)

    customColors = {
        #Gold
        #"first": [0.78,0.56,0.05,1],
        #Gold-secondary
        #"second": [0.78,0.56,0.05,0.5],
        #Jewel-primary
        #"fourth": [0.00392, 0.14117, 0.3607],

        #BLACK
        "first": [0,0,0,1],
        #BLACK
        "second": [0,0,0,1],
        #BLACK
        "black": [0,0,0,0.9],
        #WHITE
        "white": [1,1,1,1],
        
        #Casuals
        "success": [0,1,0,1],
        "failure": [1,0,0,1],
        "grey": [0.72265625,0.72265625,0.72265625,1],
        "transparent-grey": [0.72265625,0.72265625,0.72265625,.3],
        "gold": [0.78,0.56,0.05,1],
    }

    fontSizes = {
        #Big
        "primary": dp(40),

        #Medium
        "secondary": dp(30),

        #small
        "tertiary": dp(20)
    }

    spacings = {
        "none"  : dp(0),
        "small" : dp(10),
        "medium": dp(20),
        "big":dp(30)
    }

    paddings = {
        "none"  : (0,0),
        "small" : (100,50),
        "medium": (200,100),
        "big": (400,200)
    }

    appTitle = "Baca"
    navBarTitle = "Baca"


    connected = BooleanProperty()

    def __init__(self, **kwargs):
        self.title = self.appTitle
        super().__init__(**kwargs)
        self.translator = Translator()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.connected = False
        self.drone = None
        importKV_FILES()
        
        ''' if platform == 'android':
            gps.configure(on_location=self.on_gps_location)
            gps.start()
            toast("GPS on")
        else:
            currentGeocoder = geocoder.ip('me')
            try:
                self.latitude, self.longitude = currentGeocoder.latlng
                Clock.schedule_interval(self.updateLocation,1)
            except TypeError:
                log.info('Error on geolocation')
            toast("GPS only configured for Android")'''
        

    def updateLocation(self, _):
        if platform is not 'android':
            currentGeocoder = geocoder.ip('me')
            try:
                self.latitude, self.longitude = currentGeocoder.latlng
            except TypeError:
                return
                #log.info('Error on geolocation')
        else:
            gps.configure(on_location=self.on_gps_location)   
             
    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None

    def build(self):
        pass

    ##Change Screen
    def changeScreen(self,*args):
        self.root.ids.sm.push_replacement(args[0])
    

    def on_gps_location(self, *args, **kwargs):
        #  kwargs are lat, lon, speed, bearing, altitude, accuracy
        self.latitude = kwargs["lat"]
        self.longitude = kwargs["lon"]
        toast("Latitude "+self.latitude)
        toast("Longitude "+self.longitude)
        if self.latitude is not None:
            #log.info("{:.6f}".format(self.latitude))
            #log.info("{:.6f}".format(self.longitude))
            return

    def set_drone_instance(self, drone):
        self.drone = drone

    def get_drone_instance(self):
        return self.drone
    
    def set_vehicle_type(self, vehicleType):
        self.vehicleType = vehicleType

    def get_vehicle_type(self):
        return self.vehicleType
        
if __name__ == '__main__':
    ZequentMavLinkApp().run()