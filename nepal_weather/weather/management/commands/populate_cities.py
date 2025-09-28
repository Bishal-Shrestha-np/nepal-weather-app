from django.core.management.base import BaseCommand
from weather.models import PopularCity

class Command(BaseCommand):
    help = 'Populate database with popular cities in Nepal'

    def handle(self, *args, **options):
        cities_data = [
            {
                'name': 'Kathmandu',
                'name_nepali': 'काठमाडौं',
                'latitude': 27.7172,
                'longitude': 85.3240,
                'province': 'Bagmati Province'
            },
            {
                'name': 'Pokhara',
                'name_nepali': 'पोखरा',
                'latitude': 28.2096,
                'longitude': 83.9856,
                'province': 'Gandaki Province'
            },
            {
                'name': 'Lalitpur',
                'name_nepali': 'ललितपुर',
                'latitude': 27.6588,
                'longitude': 85.3247,
                'province': 'Bagmati Province'
            },
            {
                'name': 'Bharatpur',
                'name_nepali': 'भरतपुर',
                'latitude': 27.6906,
                'longitude': 84.4358,
                'province': 'Bagmati Province'
            },
            {
                'name': 'Biratnagar',
                'name_nepali': 'विराटनगर',
                'latitude': 26.4525,
                'longitude': 87.2718,
                'province': 'Province No. 1'
            },
            {
                'name': 'Birgunj',
                'name_nepali': 'वीरगञ्ज',
                'latitude': 27.0109,
                'longitude': 84.8867,
                'province': 'Madhesh Province'
            },
            {
                'name': 'Dharan',
                'name_nepali': 'धरान',
                'latitude': 26.8133,
                'longitude': 87.2833,
                'province': 'Province No. 1'
            },
            {
                'name': 'Hetauda',
                'name_nepali': 'हेटौडा',
                'latitude': 27.4280,
                'longitude': 85.0326,
                'province': 'Bagmati Province'
            },
            {
                'name': 'Janakpur',
                'name_nepali': 'जनकपुर',
                'latitude': 26.7288,
                'longitude': 85.9266,
                'province': 'Madhesh Province'
            },
            {
                'name': 'Butwal',
                'name_nepali': 'बुटवल',
                'latitude': 27.7000,
                'longitude': 83.4833,
                'province': 'Lumbini Province'
            },
            {
                'name': 'Dhangadhi',
                'name_nepali': 'धनगढी',
                'latitude': 28.7000,
                'longitude': 80.6000,
                'province': 'Sudurpashchim Province'
            },
            {
                'name': 'Mahendranagar',
                'name_nepali': 'महेन्द्रनगर',
                'latitude': 28.9644,
                'longitude': 80.1813,
                'province': 'Sudurpashchim Province'
            },
            {
                'name': 'Nepalgunj',
                'name_nepali': 'नेपालगञ्ज',
                'latitude': 28.0500,
                'longitude': 81.6167,
                'province': 'Lumbini Province'
            },
            {
                'name': 'Itahari',
                'name_nepali': 'इटहरी',
                'latitude': 26.6650,
                'longitude': 87.2722,
                'province': 'Province No. 1'
            },
            {
                'name': 'Gorkha',
                'name_nepali': 'गोर्खा',
                'latitude': 28.0000,
                'longitude': 84.6333,
                'province': 'Gandaki Province'
            },
            {
                'name': 'Bhaktapur',
                'name_nepali': 'भक्तपुर',
                'latitude': 27.6710,
                'longitude': 85.4298,
                'province': 'Bagmati Province'
            },
            {
                'name': 'Damak',
                'name_nepali': 'दमक',
                'latitude': 26.6586,
                'longitude': 87.7050,
                'province': 'Province No. 1'
            },
            {
                'name': 'Siddharthanagar',
                'name_nepali': 'सिद्धार्थनगर',
                'latitude': 27.5031,
                'longitude': 83.4613,
                'province': 'Lumbini Province'
            },
            {
                'name': 'Kalaiya',
                'name_nepali': 'कलैया',
                'latitude': 27.0326,
                'longitude': 85.0006,
                'province': 'Madhesh Province'
            },
            {
                'name': 'Tikapur',
                'name_nepali': 'टीकापुर',
                'latitude': 28.5289,
                'longitude': 81.1217,
                'province': 'Sudurpashchim Province'
            }
        ]

        created_count = 0
        updated_count = 0

        for city_data in cities_data:
            city, created = PopularCity.objects.get_or_create(
                name=city_data['name'],
                defaults=city_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created city: {city.name}')
                )
            else:
                # Update existing city data
                for field, value in city_data.items():
                    setattr(city, field, value)
                city.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated city: {city.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(cities_data)} cities:'
                f'\n- Created: {created_count}'
                f'\n- Updated: {updated_count}'
            )
        )