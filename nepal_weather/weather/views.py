# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from datetime import datetime
from decouple import config

# Load your OpenWeatherMap API key from .env
OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY')  # Make sure it's in your .env file

# Helper function for popular Nepali cities
def get_popular_cities():
    return [
        'Kathmandu', 'Pokhara', 'Lalitpur', 'Bharatpur', 'Biratnagar',
        'Birgunj', 'Dharan', 'Hetauda', 'Janakpur', 'Butwal',
        'Dhangadhi', 'Mahendranagar', 'Nepalgunj', 'Itahari', 'Gorkha'
    ]

def index(request):
    """Main weather app page (HTML)"""
    context = {
        'popular_cities': get_popular_cities(),
        'default_city': 'Kathmandu'
    }
    return render(request, 'weather/index.html', context)

@csrf_exempt
def get_cities(request):
    """API endpoint: return list of popular Nepali cities as JSON"""
    return JsonResponse({
        'success': True,
        'cities': get_popular_cities()
    })

@csrf_exempt
def get_weather(request):
    """API endpoint to get weather data from OpenWeatherMap"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        city = data.get('city', 'Kathmandu')
        weather_data = get_real_weather_data(city)
        return JsonResponse({'success': True, 'data': weather_data})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def get_real_weather_data(city):
    """Get real weather data from OpenWeatherMap API"""
    base_url = "http://api.openweathermap.org/data/2.5"

    # Current weather


    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    current_response = requests.get(current_url)
    current_data = current_response.json()

    if current_response.status_code != 200:
        raise Exception(f"Error fetching weather data: {current_data.get('message', 'Unknown error')}")

    # Forecast data
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    # Process the data
    processed_data = {
        'current': {
            'city': current_data['name'],
            'country': current_data['sys']['country'],
            'temperature': round(current_data['main']['temp']),
            'feels_like': round(current_data['main']['feels_like']),
            'humidity': current_data['main']['humidity'],
            'pressure': current_data['main']['pressure'],
            'description': current_data['weather'][0]['description'],
            'icon': current_data['weather'][0]['icon'],
            'wind_speed': current_data.get('wind', {}).get('speed', 0),
            'visibility': current_data.get('visibility', 0) / 1000,  # km
        },
        'hourly': [],
        'daily': []
    }

    # Hourly forecast (next 24 hours, 3-hour intervals)
    for item in forecast_data['list'][:8]:
        processed_data['hourly'].append({
            'time': datetime.fromtimestamp(item['dt']).strftime('%H:%M'),
            'temperature': round(item['main']['temp']),
            'description': item['weather'][0]['description'],
            'icon': item['weather'][0]['icon']
        })

    # Daily forecast (next 5 days)
    daily_data = {}
    for item in forecast_data['list']:
        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        if date not in daily_data:
            daily_data[date] = {'temps': [], 'descriptions': [], 'icons': []}
        daily_data[date]['temps'].append(item['main']['temp'])
        daily_data[date]['descriptions'].append(item['weather'][0]['description'])
        daily_data[date]['icons'].append(item['weather'][0]['icon'])

    for date, data in daily_data.items():
        day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%a')
        processed_data['daily'].append({
            'day': day_name,
            'min_temp': round(min(data['temps'])),
            'max_temp': round(max(data['temps'])),
            'description': max(set(data['descriptions']), key=data['descriptions'].count),
            'icon': max(set(data['icons']), key=data['icons'].count)
        })

    return processed_data
