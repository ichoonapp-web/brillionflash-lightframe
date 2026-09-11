from django.db import models
from django.conf import settings

class LightPreset(models.Model):
    MODE_CHOICES = [
        ('direct', 'Direct Face Illumination'),
        ('ambient', 'Surrounding/Ambient Illumination'),
        ('combined', 'Combined Illumination'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    red = models.IntegerField(default=255)
    green = models.IntegerField(default=255)
    blue = models.IntegerField(default=255)
    brightness = models.IntegerField(default=100)
    kelvin = models.IntegerField(default=6500)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='combined')
    is_trending = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    views = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='presets'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
