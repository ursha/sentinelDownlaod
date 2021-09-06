#import modules 
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import getpass
import pandas as pd
import json
import random
from ipyleaflet import Map, GeoJSON, LegendControl
import geopandas
import matplotlib.pyplot as plt
from shapely import wkt

#request for pSSWORD
password = getpass.getpass("Enter password: ")
# connect to the API
api = SentinelAPI('benasp', password, 'https://apihub.copernicus.eu/apihub')

# download single scene by known product id
#api.download(<product_id>)

# search by polygon, time, and Hub query keywords
footprint = geojson_to_wkt(read_geojson('map.geojson'))
products = api.query(footprint,
                     date = ('20210905', date(2021, 9, 6)),
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