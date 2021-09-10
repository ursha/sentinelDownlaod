#import modules 
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import getpass
import pandas as pd
import json
import random
from ipyleaflet import Map, GeoJSON, LegendControl,Marker, Popup
import geopandas
import matplotlib.pyplot as plt
from shapely import wkt
from ipywidgets import HTML
from ipyleaflet import Map, basemaps, basemap_to_tiles, DrawControl

#create a map where user creates a polygon for search area
from ipyleaflet import Map, basemaps, basemap_to_tiles, DrawControl



m =  Map(center=(50.6252978589571, 0.34580993652344), zoom=3)

draw_control = DrawControl()
draw_control.polyline =  {
    "shapeOptions": {
        "color": "#6bc2e5",
        "weight": 8,
        "opacity": 1.0
    }

}
draw_control.rectangle = {
    "shapeOptions": {
        "fillColor": "#fca45d",
        "color": "#fca45d",
        "fillOpacity": 1.0
    }
}
# 
feature_collection = {
    'type': 'FeatureCollection',
    'features': []
}
# handle drawn polygon
def handle_draw(self, action, geo_json):
    """Do something with the GeoJSON when it's drawn on the map"""    
    feature_collection['features'].append(geo_json)

draw_control.on_draw(handle_draw)

m.add_control(draw_control)

m

from geojson import  FeatureCollection, dump
feature_collection = FeatureCollection(feature_collection)
with open('myfile.geojson', 'w') as f:
   dump(feature_collection, f)


#request for pSSWORD
password = getpass.getpass("Enter password: ")
# connect to the API
api = SentinelAPI('benasp', password, 'https://apihub.copernicus.eu/apihub')

# download single scene by known product id
#api.download(<product_id>)



# search by polygon, time, and Hub query keywords
footprint = geojson_to_wkt(read_geojson('myfile.geojson'))
products = api.query(footprint,
                     date = ('20210801', date(2021, 8, 2)),
                     platformname = 'Sentinel-1')
                     #cloudcoverpercentage = (0, 30))

DataFrame= pd.DataFrame(products)
print(len(DataFrame.columns),"Products found in requested area")
print ('**********')
# for item in products:
#     print(products[item]['title'])
#     print(products[item]['summary'])
#     print(products[item]['footprint'])
products_df = api.to_dataframe(products)
#rename fotprint column to geometry 
df2 = products_df.rename({'footprint': 'geometry'}, axis=1)
# apply wkt
df2['geometry'] = df2['geometry'].apply(wkt.loads)
#add to gepandas
gdf = geopandas.GeoDataFrame(df2, geometry='geometry')
#save search results in geojson
gdf.to_file("search.geojson", driver='GeoJSON')



#plot serch results on map
with open('search.geojson', 'r') as f:
    data = json.load(f)
    


def random_color(feature):
    return {
        'color': 'black',
        'fillColor': random.choice(['red', 'yellow', 'green', 'orange']),
    }

m = Map(center=(50.6252978589571, 0.34580993652344), zoom=3)

geo_json = GeoJSON(
    data=data,
    style={
        'opacity': 1, 'dashArray': '9', 'fillOpacity': 0.1, 'weight': 1
    },
    hover_style={
        'color': 'white', 'dashArray': '0', 'fillOpacity': 0.5
    },
    style_callback=random_color
)

m.add_layer(geo_json)



m 
#done