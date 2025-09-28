
from django.contrib import admin
from .models import PopularCity, WeatherData, WeatherSearch

@admin.register(PopularCity)
class PopularCityAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_nepali', 'province', 'search_count', 'is_active']
    list_filter = ['province', 'is_active']
    search_fields = ['name', 'name_nepali', 'province']
    list_editable = ['is_active']
    ordering = ['-search_count']

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['city', 'temperature', 'description', 'updated_at']
    list_filter = ['country', 'updated_at']
    search_fields = ['city']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(WeatherSearch)
class WeatherSearchAdmin(admin.ModelAdmin):
    list_display = ['city', 'ip_address', 'search_time', 'success']
    list_filter = ['success', 'search_time']
    search_fields = ['city', 'ip_address']
    readonly_fields = ['search_time']
