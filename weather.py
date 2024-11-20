import requests
import json

def get_weather_data(city, api_key):
    # OpenWeatherMap API base URL
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Parameters for the API request
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # For temperature in Celsius
    }
    
    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Validate that all required fields exist
        if not all(key in data for key in ['main', 'weather', 'wind', 'clouds', 'sys', 'coord']):
            print("Missing required fields in weather data")
            return None
            
        return {
            'temperature': round(data['main']['temp'], 1),  # Round to 1 decimal
            'feels_like': round(data['main']['feels_like'], 1),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'wind_speed': round(data['wind']['speed'], 1),
            'wind_direction': data['wind'].get('deg', 0),
            'clouds': data['clouds']['all'],
            'sunrise': data['sys']['sunrise'],
            'sunset': data['sys']['sunset'],
            'coord': {
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon']
            }
        }
        
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error parsing weather data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    API_KEY = "82005d27a116c2880c8f0fcb866998a0"
    city = "Mumbai"
    
    weather = get_weather_data(city, API_KEY)
    if weather:
        print(f"Weather in {city}:")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Description: {weather['description']}")
        print(f"Feels Like: {weather['feels_like']}°C")
        print(f"Pressure: {weather['pressure']} hPa")
        print(f"Wind Speed: {weather['wind_speed']} m/s")
        print(f"Wind Direction: {weather['wind_direction']} degrees")
        print(f"Cloudiness: {weather['clouds']}%")
        print(f"Sunrise: {weather['sunrise']}")
        print(f"Sunset: {weather['sunset']}")
        print(f"Coordinates: {weather['coord']['lat']}, {weather['coord']['lon']}")
