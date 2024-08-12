from django.urls import path
from . import views

urlpatterns = [
    path("",views.home ,name = "home"),
    path("test_page", views.renderTest, name = "renderTest"),
    path("test", views.test, name = "testing loggin decorator"),
    path("post_test", views.put_test, name = "post testing"),
]