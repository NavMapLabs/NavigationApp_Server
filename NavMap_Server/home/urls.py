from django.urls import path
from .views import home, admin_view

urlpatterns = [
    path('', home, name='home'),
    path('temp_admin/', admin_view, name='admin_view'),
]
