import geopy
from geopy.distance import lonlat, distance, Distance
from geopy import Point
import requests
from urllib.request import urlretrieve
#from zipfile import ZipFile
import math
from typing import Dict

#define list of ordinals



def calculate_coordinates(start_point: Point, map_size: int) -> Dict[str, Point]:

    # diagonal = √2 × side
    diagonal = math.sqrt(2) * map_size
    print(f'Diagonal: {diagonal:.4f} km')
    bbox = dict()
    bbox['nw'] = start_point
    bbox['se'] = distance(kilometers=diagonal).destination(point=start_point, bearing=45)
    bbox['ne'] = Point(longitude=bbox['se'].longitude, latitude=bbox['nw'].latitude)
    bbox['sw'] = Point(longitude=bbox['nw'].longitude, latitude=bbox['se'].latitude)
    return bbox


# define start point (WGS84)
start_latitude = 51.864445  # Starting latitude in decimal degrees
start_longitude = -2.244444  # Starting longitude in decimal degrees
start_point = lonlat(x = start_longitude, y=start_latitude)

map_bbox = calculate_coordinates(start_point,2)


print(Point(map_bbox['nw']).format_decimal().split(" "))
import folium
coords = [[map_bbox['nw'].latitude,map_bbox['nw'].longitude], [map_bbox['se'].latitude,map_bbox['se'].longitude]]

# Create a map centered at the given coordinates
m = folium.Map(location=coords[0], zoom_start=13)

# Sample coordinates

# Create a Rectangle object
rectangle = folium.Rectangle(
    bounds=coords,
    color='#ff7800',
    fill=True,
    fill_color='#ffff00',
    fill_opacity=0.2
)

# Add the rectangle to the map
rectangle.add_to(m)
tile = folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite',
    overlay=False,
    control=True
).add_to(m)
folium.GeoJson("elevation_data.geojson", name="Elevation").add_to(m)

# Add layer control
folium.LayerControl().add_to(m)
# Display the map
m.save("tst.html")
import webbrowser
webbrowser.open('tst.html')
