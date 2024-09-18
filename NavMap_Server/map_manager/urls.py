from django.urls import path
from . import views

urlpatterns = [
    path("put_test", views.put_test, name = "post testing"),
    path("get_user_info", views.get_user_info, name = "get user info"),
    path("update_map", views.update_map, name = "update map"),
    path("get_map", views.get_map, name = "get map"),
    path("grant_edit_permission", views.grant_edit_permission, name = "give edit permission"),
    path("create_map", views.dev_create_map, name = "create map"),
]