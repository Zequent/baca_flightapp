from kivy_garden.mapview import MapView, MapMarker, MapSource
import geocoder
currentGeocoder = geocoder.ip('me')
from kivymd.app import MDApp



class ZequentMapView(MapView):

   
    app=MDApp.get_running_app()
    latitude = 47.28876860219628
    longitude = 11.14698035747897
   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zoom=22
        self.lat = self.latitude
        self.lon = self.longitude

        apiKey = 'AIzaSyBSwt7u9Pn-Hw09bWsiQ-ZQqlE7aGf5Gxg'
        session = 'AJVsH2xGGYNwrRk_cn8hF5AKWVbN527eF2s3013IJJT9WZWRANmAVTT_ZIz5IFzRQYrkH6oDdo2Zc4E9QJwkl8ih_w'
        source = MapSource(url='https://tile.googleapis.com/v1/2dtiles/{z}/{x}/{y}?key='+apiKey + '&session=' + session,
                            cache_key="google-maps", tile_size=256,
                            image_ext="jpeg", attribution="@GoogleMaps")
        self.map_source = source
        self.lat = self.latitude
        self.lon = self.longitude
        #self.updateMap()
        
    
    def updateMap(self):
        if(self.app is not None ):
            self.latitude = self.app.latitude
            self.longitude = self.app.longitude
            
        self.center_on(self.latitude, self.longitude)


    
    def build(self):
        pass