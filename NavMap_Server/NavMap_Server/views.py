from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

def index(requeset):
    return HttpResponse("Home Page")