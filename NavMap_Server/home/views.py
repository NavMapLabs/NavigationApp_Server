from django.http import HttpResponse
from django.shortcuts import render
from authApp.decorators import role_required

# Create your views here.
def home(request):
    return HttpResponse("Hello, Welcome to the Homepage")

@role_required('admin')
def admin_view(request):
    return render(request, 'authApp/admin_view.html')