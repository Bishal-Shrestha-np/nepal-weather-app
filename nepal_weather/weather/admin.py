
from django.contrib import admin
from .models import PopularCity, WeatherData, WeatherSearch

@admin.register(PopularCity)
class PopularCityAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_nepali', 'province', 'search_count', 'is_active']
    list_filter = ['province', 'is_active']
    search_fields = ['name', 'name_nepali', 'province']
    list_editable = ['is_active']
    ordering = ['-search_count']

