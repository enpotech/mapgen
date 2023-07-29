import requests
base_url = 'https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer/exportImage'

# Define the parameters for the NAIP image download
params = {
    'bbox': '-118.5,33.8,-118.3,34.1',
    'size': '1000,1000',
    'format': 'jpg',
    'f': 'image'
}

# Send the API request
response = requests.get(base_url, params=params)
if response.status_code == 200:
    # The request was successful
    # Save the image content to a file
    with open('naip_image.jpg', 'wb') as f:
        f.write(response.content)
    print('Image saved successfully.')
else:
    # The request was unsuccessful
    print('Request failed with status code:', response.status_code)
