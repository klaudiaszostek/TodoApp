from flask import request

def fetch_weather():
    # Podstawowy przykład API OpenWeatherMap (musisz się zarejestrować i uzyskać API key)
    api_key = 'your_api_key'
    city = 'Krakow'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = request.get(url)
    data = response.json()
    
    if response.status_code == 200:
        return {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'city': city
        }
    return None
