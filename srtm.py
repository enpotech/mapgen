import folium
from folium import raster_layers

# Example SRTM elevation data (replace this with your actual data)
# For demonstration purposes, we're using a simple 3x3 grid of elevation values.
srtm_elevation_data = [
    [100, 150, 120],
    [140, 180, 130],
    [110, 160, 90],
]

# Latitude and Longitude of the center point for the Folium map
latitude, longitude = 38.8895, -77.0352  # Replace with your desired location

# Create a Folium map centered at the specified location
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# Add OpenStreetMap tiles as the base layer
folium.TileLayer('openstreetmap').add_to(m)

# Add SRTM elevation data as an overlay on top of the base layer
# Adjust the bounds parameter to fit your data appropriately
raster_layers.ImageOverlay(
    image=srtm_elevation_data,
    bounds=[[latitude - 0.001, longitude - 0.001], [latitude + 0.001, longitude + 0.001]],
    colormap=lambda x: (1, 0, 0, x/255),  # Example colormap (red tones)
).add_to(m)

# Save the map to an HTML file
m.save("srtm_map.html")
