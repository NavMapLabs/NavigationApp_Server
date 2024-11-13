from django.db import models

class user(models.Model):
    ACCESS_LEVEL = {
        1 : "Normal User",
        2 : "Map Editor",
        3 : "Map Manager"
    }
    uid = models.CharField(max_length=200, primary_key=True, verbose_name= "user id")
    user_name = models.CharField(max_length=100, default= None, verbose_name="user name")
    permission_level =models.IntegerField(choices= ACCESS_LEVEL, default=1, verbose_name='Permission Level')
