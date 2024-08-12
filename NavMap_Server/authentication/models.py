from django.db import models

# Create your models here.
class userPermission(models.Model):
    ACCESS_LEVEL = {
        1 : "Anonymous User",
        2 : "Normal User",
        3 : "Map Editor"
    }
    uid = models.CharField(max_length=100)
    level =models.IntegerField(choices= ACCESS_LEVEL)

class map_editor(models.Model):
    uid = models.CharField(max_length=100)
    map = models.CharField(max_length=100)
    
class map_data(models.Model):
    map = models.CharField(max_length=100)
    map_data = models.CharField(max_length=100)