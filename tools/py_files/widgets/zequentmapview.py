from kivy_garden.mapview import MapView, MapMarker, MapSource
import geocoder
from zequentmavlinklib.ArduPlane import ArduPlaneObject
from kivy.properties import NumericProperty


currentGeocoder = geocoder.ip('me')
from kivymd.app import MDApp


class ZequentMapView(MapView):
    latitude = NumericProperty(47.28692205219049)
    longitude = NumericProperty(11.147142586915848)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.zoom = 22
        self.marker = MapMarker(lat = self.latitude, lon = self.longitude)
        self.marker.source = "./static/icons/drone_icon.png"
        self.add_marker(marker=self.marker)
        self.drone: ArduPlaneObject = self.app.drone
        pos = self.drone.get_current_pos()

        print(str(self.lat) + " " + str(self.lon))
        

        self.center_on(self.latitude, self.longitude)
        # self.updateMap()

    def change_marker(self, templat, templon):
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
