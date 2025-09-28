from django.db import models
from django.utils import timezone
from datetime import timedelta

class PopularCity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_nepali = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    province = models.CharField(max_length=100)
    search_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-search_count', 'name']
        verbose_name_plural = "Popular Cities"

    def __str__(self):
        return f"{self.name} ({self.province})"

    def increment_search_count(self):
        self.search_count += 1
        self.save(update_fields=['search_count'])

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=10, default='NP')
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    description = models.CharField(max_length=200)
    icon_code = models.CharField(max_length=10)
    wind_speed = models.FloatField()
    visibility = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['city', 'country']
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"

    def is_cache_valid(self, minutes=30):
        """Check if cached weather data is still valid"""
        return timezone.now() - self.updated_at < timedelta(minutes=minutes)

class WeatherSearch(models.Model):
    city = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    search_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)

    class Meta:
        ordering = ['-search_time']

    def __str__(self):
        return f"{self.city} - {self.search_time.strftime('%Y-%m-%d %H:%M')}"