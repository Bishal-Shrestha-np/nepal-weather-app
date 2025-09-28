from django.core.management.base import BaseCommand
from weather.models import PopularCity
from weather.utils.weather_api import WeatherAPIClient
import time

class Command(BaseCommand):
    help = 'Fetch weather data for all cities'

    def add_arguments(self, parser):
        parser.add_argument('--city', type=str, help='Specific city to update')
        parser.add_argument('--limit', type=int, default=10, help='Limit number of cities')

    def handle(self, *args, **options):
        api_client = WeatherAPIClient()
        
        if options['city']:
            cities = PopularCity.objects.filter(name__icontains=options['city'])[:1]
        else:
            cities = PopularCity.objects.filter(is_active=True)[:options['limit']]

        for city in cities:
            try:
                weather_data = api_client.get_current_weather(city.name)
                if weather_data:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated weather for {city.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed to update weather for {city.name}')
                    )
                time.sleep(1)  # Rate limiting
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error updating {city.name}: {str(e)}')
                )