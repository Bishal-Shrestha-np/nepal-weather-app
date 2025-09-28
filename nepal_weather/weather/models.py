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

