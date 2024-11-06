from django.urls import path
from . import views

urlpatterns = [
    path('upload_photo', views.upload_photo, name='upload_photo'),
    path('get_photos', views.get_photos, name='get_photos'),
    path('get_photo', views.get_photos_by_title, name='get_photos_by_title'),
]