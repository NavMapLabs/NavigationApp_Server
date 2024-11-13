from django.db import models
from authentication.models import user
import uuid

class maps(models.Model):
    map_name = models.CharField(max_length=100, primary_key=True)
    map_addr = models.CharField(max_length=100)
    map_description = models.CharField(max_length=200)
    

# map with specific version
class map_variation(models.Model):
    map_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    version_name = models.CharField(max_length=100, default = "")
    map_info = models.ForeignKey(maps, on_delete=models.CASCADE, related_name='variations', to_field='map_name')
    map_editor =models.ForeignKey(user, on_delete=models.DO_NOTHING, related_name='map_uploaded')
    map_data = models.CharField(max_length=5000, default = "")
    modified_date = models.DateTimeField(auto_now=True)

    