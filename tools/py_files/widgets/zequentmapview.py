from kivy_garden.mapview import MapView, MapMarker, MapSource
import geocoder
from zequentmavlinklib.ArduPlane import ArduPlaneObject
from kivy.properties import NumericProperty
from kivymd.icon_definitions import md_icons

from tools.Utils import Utils


currentGeocoder = geocoder.ip('me')
from kivymd.app import MDApp


class ZequentMapView(MapView):
    latitude = NumericProperty(47.28692205219049)
    longitude = NumericProperty(11.147142586915848)

    home_pos_lat = 0
    home_pos_lon = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.drone: ArduPlaneObject = self.app.drone
        self.zoom = 22
        droneIcon = Utils.get_drone_icon(self.app.get_vehicle_type())

        self.marker = MapMarker(lat = self.latitude, lon = self.longitude)
        self.marker.source = droneIcon
        
        self.penultimate = MapMarker(lat = self.latitude, lon = self.longitude)
        self.penultimate.source = droneIcon
        self.penultimate.opacity = .5

        self.last = MapMarker(lat = self.latitude, lon = self.longitude)
        self.last.source = droneIcon
        self.last.opacity = .2

        #Home Pos marker
        home_pos_icon_source = MapMarker
        response = self.drone.get_home_pos()
        home_pos_lat = response.latitude * 0.0000001
        home_pos_lon = response.longitude * 0.0000001

        self.home_pos_marker = MapMarker(lat = home_pos_lat, lon =home_pos_lon)
        self.home_pos_marker.source = './static/icons/baseline_home_white_24dp.png'

        self.add_marker(marker=self.marker)
        self.add_marker(marker=self.penultimate)
        self.add_marker(marker=self.last)
        self.add_marker(marker=self.home_pos_marker)
        self.drone: ArduPlaneObject = self.app.drone
       
        print(str(self.lat) + " " + str(self.lon))
        

        self.center_on(self.latitude, self.longitude)
        # self.updateMap()

    def change_pos_marker(self, templat, templon):
        self.last.lat = self.penultimate.lat
        self.last.lon = self.penultimate.lon
        
        self.penultimate.lat = self.marker.lat
        self.penultimate.lon = self.marker.lon

        self.marker.lat = templat
        self.marker.lon = templon
        self.center_on(templat, templon)

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
