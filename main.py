import geopy
from geopy.distance import lonlat, distance, Distance
from geopy import Point
import requests
from urllib.request import urlretrieve
#from zipfile import ZipFile
import math

#define list of ordinals
bbox_ordinals = ['ne', 'se', 'sw', 'nw']
map_size = 2 #size in km

def calculate_coordinates(start_point: Point):

    # diagonal = √2 × side
    diagonal = math.sqrt(2) * map_size
    print(f'Diagonal: {diagonal:.4f}')
    bbox = dict.fromkeys(bbox_ordinals)
    bbox['nw'] = start_point
    bbox['se'] = distance(kilometers=diagonal).destination(point=start_point, bearing=45)
    bbox['ne'] = Point(longitude=bbox['se'].longitude, latitude=bbox['nw'].latitude)
    bbox['sw'] = Point(longitude=bbox['nw'].longitude, latitude=bbox['se'].latitude)

    return bbox

start_latitude = 48.86104478375485  # Starting latitude in decimal degrees
start_longitude = -98.95309028761801  # Starting longitude in decimal degrees
start_point = lonlat(x = start_longitude, y=start_latitude)

map_bbox = calculate_coordinates(start_point)



print(f"Starting coordinates: {Point(map_bbox['nw']).format_decimal()}")
print(f"Destination coordinates: {Point(map_bbox['se']).format_decimal()}")

print(f"Start lat: {start_point.latitude:.4f}")
print(f"Start lon: {start_point.longitude:.4f}")


# print(f"end lat: {end_point.latitude:.6f}")
# print(f"end lon: {end_point.longitude}")

# ne_corner = Point(latitude=start_point.latitude, longitude=end_point.latitude)
# sw_corner = Point(latitude=end_point.latitude, longitude=end_point.longitude)
# se_corner = Point(latitude=start_point.latitude, longitude=end_point.longitude)

# bbox = f'{start_point.longitude:.6f},{start_point.latitude:.6f},{end_point.longitude:.6f},{end_point.latitude:.6f}'
# print(bbox)
# datasets = 'National+Elevation+Dataset+(NED)+1/9+arc-second'
# url = f'https://tnmaccess.nationalmap.gov/api/v1/products?bbox={bbox}&datasets={datasets}&max=400'

# def getme(url):
#     print(url)
#     filename = url.split('/')[-1]
#     urlretrieve(url,filename)
#     with ZipFile(filename, 'r') as zipObj:
#         zipObj.extract(filename.replace('.zip','.img'))


# response = requests.get(url)
# list(map(lambda x: print(x['downloadURL']), response.json()['items']))
# #list(map(lambda x: getme(x['downloadURL']), response.json()['items']))

