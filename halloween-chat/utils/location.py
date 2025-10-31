import requests

def get_user_location():
    try:
        response = requests.get('https://ipapi.co/json/')
        data = response.json()
        return {
            'city': data.get('city', 'Unknown City'),
            'country': data.get('country_name', 'Unknown Land'),
            'lat': data.get('latitude'),
            'lng': data.get('longitude')
        }
    except:
        return {
            'city': 'Unknown City', 
            'country': 'Unknown Land',
            'lat': None,
            'lng': None
        }