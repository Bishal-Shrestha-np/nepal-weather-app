from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/weather/', views.get_weather, name='get_weather'),
    path('city/<str:city_name>/', views.get_weather, name='city_weather'),  # reuses get_weather
    path('api/cities/', views.get_cities, name='get_cities'),
]
