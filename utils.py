#from zipfile import ZipFile
import math
from typing import Dict
from urllib.request import urlretrieve

import geopy
import requests
from geopy import Point
from geopy.distance import Distance, distance, lonlat
import folium
#define list of ordinals
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from PIL import Image, ImageFilter
from rasterio.plot import reshape_as_image
import requests

def calculate_coordinates(start_point: Point, map_size: float) -> Dict[str, Point]:

    # diagonal = √2 × side
    diagonal = math.sqrt(2) * map_size
    print(f'Diagonal: {diagonal:.4f} km')
    bbox = dict()
    bbox['nw'] = start_point
    bbox['se'] = distance(kilometers=diagonal).destination(point=start_point, bearing=135)
    bbox['ne'] = Point(longitude=bbox['se'].longitude, latitude=bbox['nw'].latitude)
    bbox['sw'] = Point(longitude=bbox['nw'].longitude, latitude=bbox['se'].latitude)
    return bbox


# define start point (WGS84)
start_latitude = 51.864445  # Starting latitude in decimal degrees
start_longitude = -2.244444  # Starting longitude in decimal degrees
start_point = lonlat(x = start_longitude, y=start_latitude)

map_bbox = calculate_coordinates(start_point,2)

def download_srtm_data(api_key, south, north, west, east, output_file):
    try:

        # url = f"https://portal.opentopography.org/API/globaldem?demtype=SRTMGL1&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&API_Key={api_key}"
        url = f"https://server.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{13}/{2}/{50}"
        url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{18}/{}/{x}"
        # Send an HTTP GET request to the OpenTopography API
        response = requests.get(url)
        response.raise_for_status()

        # Save the data to a local file
        with open(output_file, 'wb') as f:
            f.write(response.content)

        print(f"SRTM data downloaded successfully to '{output_file}'")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

api_key = "ee95e75d42fbad761ddc4af359bd941a"

output_file = "srtm_data.tif"  # Replace with the desired output file path

south = map_bbox["sw"].latitude
north = map_bbox["nw"].latitude
west = map_bbox["sw"].longitude
east = map_bbox['ne'].longitude
print(south, north, west, east,)
print(f'https://www.gmrt.org/services/GridServer?north={north}&west={west}&east={east}&south={south}&layer=topo&format=geotiff&mresolution=1')

download_srtm_data(api_key, south, north, west, east, output_file)


def geotiff_to_grayscale_with_blur(geotiff_file, output_jpeg):
    try:
        # Read the GeoTIFF file
        with rasterio.open(geotiff_file) as dataset:
            # Read the single-band raster data
            data = dataset.read(1)

            # Limit the range of values to avoid exaggeration
            vmin = np.percentile(data, 0)   # 5th percentile as minimum value
            vmax = np.percentile(data, 100)  # 95th percentile as maximum value
            clipped_data = np.clip(data, vmin, vmax)

            # Normalize the data to 0-255 range
            normalized_data = ((clipped_data - vmin) / (vmax - vmin) * 255).astype(np.uint8)

        # Convert NumPy array to PIL Image
        image = Image.fromarray(normalized_data, mode='L')  # 'L' mode for grayscale

        # Apply Gaussian blur to the image
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=2))

        # Save the PIL Image as JPEG
        blurred_image.save(output_jpeg, format='PNG')

        print(f"GeoTIFF converted to grayscale and saved as JPEG: '{output_jpeg}'")
    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage
geotiff_file = "srtm_data.tif"  # Replace with the path to your GeoTIFF file
output_jpeg = "output_image.png"
geotiff_to_grayscale_with_blur(geotiff_file, output_jpeg)

coords = [[map_bbox['nw'].latitude,map_bbox['nw'].longitude], [map_bbox['se'].latitude,map_bbox['se'].longitude]]
print(map_bbox['se'].longitude)
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

tiledem = folium.TileLayer(
    tiles='https://server.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri DEM',
    overlay=False,
    control=True
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)
# Display the map
m.save("tst.html")
import webbrowser

webbrowser.open('tst.html')
