from django.db import models
# Create your models here.

# class user(models.Model):
#     uid = models.CharField(max_length=150, primary_key=True)
#     username = models.CharField(max_length=150)
#     verified_status = models.BooleanField() #need to be verified to be editor/manager?
#     history = models.CharField(max_length = 500, default= "") # should be a list of maps' names
#     editable_map = models.CharField(max_length = 500, default= "") # should be a list of maps' names
#     managed_map = models.CharField(max_length = 500, default= "") # should be a list of maps' names

# for managers or verified user only

class user(models.Model):
    ACCESS_LEVEL = {
        1 : "Normal User",
        2 : "Map Editor",
        3 : "Map Manager"
    }
    uid = models.CharField(max_length=200, primary_key=True)
    user_name = models.CharField(max_length=100, default= None)
    permission_level =models.IntegerField(choices= ACCESS_LEVEL, default=1)
    # email = models.CharField(max_length=150)
    # phone = models.CharField(max_length=150)
    # Legal_name = models.CharField(max_length=150)
