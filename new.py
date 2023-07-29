import ee, requests, io
#ee.Authenticate()

ee.Initialize()
print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())

# A Sentinel-2 surface reflectance image.
img = ee.Image('COPERNICUS/S2_SR/20210109T185751_20210109T185931_T10SEG')
#img = ee.image('USDA/NAIP/DOQQ')

# A small region within the image.
region = ee.Geometry.BBox(-122.0859, 37.0436, -122.0626, 37.0586)

img.get("title").getInfo()

# Image chunk as a NumPy structured array.
import numpy
url = img.getDownloadUrl({
    'bands': ['R', 'G', 'B'],
    'region': region,
    'scale': 20,
    'format': 'NPY'
})
response = requests.get(url)
data = numpy.load(io.BytesIO(response.content))
print(data)
print(data.dtype)

# Single-band GeoTIFF files wrapped in a zip file.
url = img.getDownloadUrl({
    'name': 'single_band',
    'bands': ['R', 'G', 'B'],
    'region': region
})
response = requests.get(url)
with open('single_band.zip', 'wb') as fd:
  fd.write(response.content)

# Multi-band GeoTIFF file wrapped in a zip file.
url = img.getDownloadUrl({
    'name': 'multi_band',
    'bands': ['R', 'G', 'B'],
    'region': region,
    'scale': 20,
    'filePerBand': False
})
response = requests.get(url)
with open('multi_band.zip', 'wb') as fd:
  fd.write(response.content)

# Band-specific transformations.
url = img.getDownloadUrl({
    'name': 'custom_single_band',
    'bands': [
        {'id': 'R', 'scale': 10},
        {'id': 'G', 'scale': 10},
        {'id': 'B', 'scale': 10}
    ],
    'region': region
})
response = requests.get(url)
with open('custom_single_band.zip', 'wb') as fd:
  fd.write(response.content)

# Multi-band GeoTIFF file.
url = img.getDownloadUrl({
    'bands': ['R', 'G', 'B'],
    'region': region,
    'scale': 20,
    'format': 'GEO_TIFF'
})
response = requests.get(url)
with open('multi_band.tif', 'wb') as fd:
  fd.write(response.content)