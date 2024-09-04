from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from . import models
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def home(request):
    return HttpResponse("Hello\n")

def renderTest(request):
    return render(request ,'placeholder.html')

@csrf_exempt
def test(request):
    
    if 'user_name' in request.session:
        name = request.session["user_name"]
        data = { "message": name }
    else:
        data = { "message": "no session" }
    print(data)
    return JsonResponse(data)

@csrf_exempt
@require_http_methods(['PUT'])
def put_test(request):
    user = request.user
    # if user is has account, get the permission, if has permission then can post data of the map
    if (user.is_authenticated):
        data = request.body
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                query_map = data["map"]
                update_data = data["map_data"]
                print(query_map)
                print(update_data)
            except json.JSONDecodeError:
                return HttpResponse("decode error", status = 400)
        else :
            print("not json data")
        permission = models.userPermission.objects.get(uid = user.username)
        if permission == None or permission.level != 3:
            return HttpResponse("Permission denied: No edit permission\n",status = 403)
        else:
            if models.map_editor.objects.filter(uid = user.username, map = query_map).exists():
                map = models.map_data.objects.get(map = query_map)
                map.map_data = update_data
                map.save()
                return HttpResponse("success\n", status = 200)
            else:
                message = "Permission denied: No '" + query_map + "' edit rights\n"
                return HttpResponse(message,status = 403)
        return HttpResponse("ok\n",status = 200)
        
    else:
        return HttpResponse("Permission denied\n",status = 403)
        