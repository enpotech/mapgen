from srtm import Srtm1HeightMapCollection

# Set the path to the directory where the SRTM data will be stored
import os
os.environ["SRTM1_DIR"] = "/path/to/srtm1/"

# Create an instance of the Srtm1HeightMapCollection class
srtm1_data = Srtm1HeightMapCollection()

# Get the altitude at a specific location
latitude = 40.123
longitude = -7.456
altitude = srtm1_data.get_altitude(latitude=latitude, longitude=longitude)

print(f"The altitude at {latitude}, {longitude} is {altitude} meters.")