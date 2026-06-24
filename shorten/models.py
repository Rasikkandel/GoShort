from django.db import models
from django.utils import timezone

# Create your models here.
class long_urls(models.Model):
    long_url = models.URLField(max_length=2048, unique=False)
    short_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.short_code} -> {self.long_url}" 