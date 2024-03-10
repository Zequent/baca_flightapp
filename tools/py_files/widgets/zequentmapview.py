from kivy_garden.mapview import MapView, MapMarker, MapSource
import geocoder

currentGeocoder = geocoder.ip('me')
from kivymd.app import MDApp


class ZequentMapView(MapView):
    app = MDApp.get_running_app()
    latitude = 47.28692205219049
    longitude = 11.147142586915848

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zoom = 22

        print(str(self.lat) + " " + str(self.lon))
        

        self.center_on(self.latitude, self.longitude)
        # self.updateMap()

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
