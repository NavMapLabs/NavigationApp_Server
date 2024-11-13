from django.urls import path
from . import views

urlpatterns = [
    path("get_user_info", views.get_user_info, name = "get_user_info"),
    path("update_map", views.update_map, name = "update_map"),
    path("get_map_meta_info", views.get_map_meta_info, name = "get_map"),
    path("get_map_data", views.id_to_data, name = "get_map_data"),
    path("grant_edit_permission", views.grant_edit_permission, name = "give_edit_permission"),
    path("create_map", views.dev_create_map, name = "create_map"),
    path("delete_map", views.delete_map, name = "delete_map"),
    path("id_to_meta", views.id_to_meta, name = "get_map_meta_from_id"),
]