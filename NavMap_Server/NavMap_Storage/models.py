from django.db import models

class MapPhoto(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    google_drive_id = models.CharField(max_length=255, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)