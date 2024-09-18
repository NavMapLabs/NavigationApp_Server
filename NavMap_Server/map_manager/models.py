from django.db import models

# Create your models here.
class map_editor(models.Model):
    uid = models.CharField(max_length=100)
    map = models.CharField(max_length=100)
    
class map_data(models.Model):
    map = models.CharField(max_length=100)
    map_data = models.CharField(max_length=100)

class map(models.Model):
    name = models.CharField( max_length = 500, primary_key= True)
    editor = models.CharField(max_length = 500, default= "") # should be a list
    manager = models.CharField(max_length = 500) # should be a list
    edges = models.CharField(max_length = 100, default= "") # should be a list of  pairs of coordinate
    node = models.CharField( max_length = 100, default= "") # should be a list of coordinates
    map_description = models.CharField(max_length = 500, default= "") # should be a list of coordinates
    