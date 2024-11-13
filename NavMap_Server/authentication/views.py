from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from . import models as authmodels
from map_manager import models
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def login(request):
    if not request.user.is_authenticated:
        return HttpResponse("user is not logged in")
    else:
        return HttpResponse("User is logged in")

@csrf_exempt
def test(request):
    if 'uid' in request.session:
        name = request.session["uid"]
        data = { "message": name }
    else:
        data = { "message": "no session" }
    return JsonResponse(data)


        