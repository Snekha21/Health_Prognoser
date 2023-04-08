import requests

opencage_api_key = '510f29bf21b44ba6a7e39b4f0275f902'  # replace with your API key
latitude = 37.7749  # replace with the latitude of your location
longitude = -122.4194  # replace with the longitude of your location

opencage_url = 'https://api.opencagedata.com/geocode/v1/json'
params = {
    'q': f"{latitude}, {longitude}",
    'key': opencage_api_key,
    'no_annotations': 1
}
response = requests.get(opencage_url, params=params)
if response.status_code == 200:
    data = response.json()
    if len(data['results']) > 0:
        query = 'hospitals'  # search query for hospitals
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        radius = 5000  # search radius in meters
        opencage_url = 'https://api.opencagedata.com/places/v1/discover/explore'
        params = {
            'q': query,
            'location': f"{latitude},{longitude}",
            'radius': radius,
            'key': opencage_api_key,
            'no_annotations': 1
        }
        response = requests.get(opencage_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                hospitals = data['results']
                for hospital in hospitals:
                    print(hospital['name'])
            else:
                print("No hospitals found.")
        else:
            print("Error connecting to OpenCage API.")
    else:
        print("No location found.")
else:
    print("Error connecting to OpenCage API.")

