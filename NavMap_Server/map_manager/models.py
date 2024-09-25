from django.db import models
from authentication.models import user
import uuid

class maps(models.Model):
    map_name = models.CharField(max_length=100)
    map_addr = models.CharField(max_length=100)
    map_description = models.CharField(max_length=200)

# map with specific version
class map_variation(models.Model):
    map_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    version_name = models.CharField(max_length=100, default = "")
    map_info = models.ForeignKey(maps, on_delete=models.CASCADE, related_name='variations')
    map_editor =models.ForeignKey(user, on_delete=models.DO_NOTHING, related_name='map_uploaded')
    map_data = models.CharField(max_length=100, default = "")


# class map(models.Model):
#     name = models.CharField( max_length = 500, primary_key= True)
#     editor = models.CharField(max_length = 500, default= "") # should be a list
#     manager = models.CharField(max_length = 500) # should be a list
#     edges = models.CharField(max_length = 100, default= "") # should be a list of  pairs of coordinate
#     node = models.CharField( max_length = 100, default= "") # should be a list of coordinates
#     map_description = models.CharField(max_length = 500, default= "") # should be a list of coordinates
    