from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return HttpResponse("Hello\n")

def renderTest(request):
    return render(request ,'placeholder.html')

@login_required
def test(request):
    print(request.user.is_authenticated)
    return(HttpResponse("logged in\n"))
    # keys = request.GET.get("data")
    # data = "data"
    # if fields:
    #     fields = fields.split(',')
    # return JsonResponse(list(data), safe= False)
        