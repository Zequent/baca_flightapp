import threading
from kivy_garden.mapview import MapView, MapMarker, MapSource, MapMarkerPopup
import geocoder
from zequentmavlinklib.ArduPlane import ArduPlaneObject
from zequentmavlinklib.Globals import WorkerThread
from kivy.properties import NumericProperty
from tools.Utils import Utils
from kivy.clock import mainthread
from kivy.metrics import dp
from tools.py_files.widgets.zequentbutton import ZequentButton
currentGeocoder = geocoder.ip('me')
from kivymd.app import MDApp
from logging import getLogger
import logging

import cv2  # importing cv 
import imutils 
log = getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)  
class ZequentMapView(MapView):
    latitude = NumericProperty(47.28692205219049)
    longitude = NumericProperty(11.147142586915848)

    home_pos_lat = 0
    home_pos_lon = 0
    
    tempRoatationMarkerArray = [] 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.drone: ArduPlaneObject = self.app.drone
        self.zoom = 22
        self.droneIcon = Utils.get_drone_icon(self.app.get_vehicle_type())

        self.marker = MapMarkerPopup(lat = self.latitude, lon = self.longitude)
        self.marker.source = self.droneIcon
        button = ZequentButton(text="dafasdf")
        self.marker.add_widget(button)
        self.marker.popup_size = dp(250), dp(250)
        
        
        self.penultimate = MapMarker(lat = self.latitude, lon = self.longitude)
        self.penultimate.source = self.droneIcon
        self.penultimate.opacity = .5

        self.last = MapMarker(lat = self.latitude, lon = self.longitude)
        self.last.source = self.droneIcon
        self.last.opacity = .2

        #Home Pos marker
        response = self.drone.get_home_position()
        home_pos_lat = response.latitude * 0.0000001
        home_pos_lon = response.longitude * 0.0000001

        self.home_pos_marker = MapMarker(lat = home_pos_lat, lon =home_pos_lon)
        self.home_pos_marker.source = './static/icons/baseline_home_white_24dp.png'

        self.add_marker(marker=self.marker)
        self.add_marker(marker=self.penultimate)
        self.add_marker(marker=self.last)
        self.add_marker(marker=self.home_pos_marker)

        log.info(str(self.lat) + " " + str(self.lon))
        

        self.center_on(self.latitude, self.longitude)
        # self.updateMap()

    def change_pos_marker(self, templat, templon, hdg):
        threading.Thread(target=self.update_marker, args=[hdg]).start()
        self.last.lat = self.penultimate.lat
        self.last.lon = self.penultimate.lon
        
        self.penultimate.lat = self.marker.lat
        self.penultimate.lon = self.marker.lon

        self.marker.lat = templat
        self.marker.lon = templon
        self.center_on(templat, templon)

    @mainthread
    def update_marker(self, hdg):
        
        hdg = int(hdg)

        if hdg % 2 == 1:
            return

        fileName = './static/icons/cache/temp_rotation_'+str(int(hdg))+'_.png'
        #Change rotation of image !!! WORKS NOT CLOCKWISE !!!
        newAngle = hdg*-1
        image = cv2.imread(self.droneIcon, cv2.IMREAD_UNCHANGED) 
        Rotated_image = imutils.rotate(image, angle=newAngle) 
        cv2.imwrite(fileName, Rotated_image) 

        #CHANGE ICONS
        self.marker.source = fileName

        if len(self.tempRoatationMarkerArray) <= 2 :
            self.tempRoatationMarkerArray.append(fileName)
        else:
            self.last.source = self.tempRoatationMarkerArray.pop(0)
            self.penultimate.source = self.tempRoatationMarkerArray.pop(0)
        

    def setSatelitteMode(self):
        self.apiKey = 'AIzaSyBSwt7u9Pn-Hw09bWsiQ-ZQqlE7aGf5Gxg'
        self.session = 'AJVsH2xGGYNwrRk_cn8hF5AKWVbN527eF2s3013IJJT9WZWRANmAVTT_ZIz5IFzRQYrkH6oDdo2Zc4E9QJwkl8ih_w'
        self.source = MapSource(
        url='https://tile.googleapis.com/v1/2dtiles/{z}/{x}/{y}?key=' + self.apiKey + '&session=' + self.session,
        cache_key="google-maps", tile_size=256,
        image_ext="jpeg", attribution="@GoogleMaps")

        self.map_source = self.source
    
    def setSatelitteMode(self):
        self.apiKey = 'AIzaSyBSwt7u9Pn-Hw09bWsiQ-ZQqlE7aGf5Gxg'
        self.session = 'AJVsH2xGGYNwrRk_cn8hF5AKWVbN527eF2s3013IJJT9WZWRANmAVTT_ZIz5IFzRQYrkH6oDdo2Zc4E9QJwkl8ih_w'
        self.source = MapSource(
        url='https://tile.googleapis.com/v1/2dtiles/{z}/{x}/{y}?key=' + self.apiKey + '&session=' + self.session,
        cache_key="google-maps", tile_size=256,
        image_ext="jpeg", attribution="@GoogleMaps")

        self.map_source = self.source

    def setDefaultMode(self):
        self.map_source = 'osm'

    def updateMap(self):
        if (self.app is not None):
            self.latitude = self.app.latitude
            self.longitude = self.app.longitude

        self.center_on(self.latitude, self.longitude)

    def build(self):
        pass
