from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from . import models
from authentication import models as authmodels
import json
# ---------------------------------- helper function -----------------------------------
def update_user_history(user, map_name):
    # if within 10 append, if not pop the last one and preppend
    pass

# auth user and map user are two independent tables, make sure the first time user create the entry
def create_user_entry(request):
    if authmodels.user.objects.filter(uid = request.user.username).exists():
        return
    #for now, uid and username is actually not the same
    # todo: change store the uid and username in the session during firebase middleware token verification phase, then update here
    authmodels.user.objects.create(uid = request.user.username, username = request.user.username, verified_status = False)
    return
# ---------------------------------- end of helper function -----------------------------------

# return the maps that match with the search, no auth needed
@require_http_methods(['GET'])
def search(request):
    # return the list of matched map name (maybe the description)
    #--todo -------
    pass


# return the edge and node data to the frontend, no auth needed
@require_http_methods(['GET'])
def get_map(request):
    create_user_entry(request)
    data = request.body
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            data_type = data["data_type"]
            if data_type != "Map_request":
                raise json.JSONDecodeError
            data = data["data"]
            map_name = data["map_name"]
        except json.JSONDecodeError:
            return HttpResponse("key error", status = 400)
    else :
        return HttpResponse("Wrong data content type, only accept json\n",status = 400)
    # get data
    map = models.map.objects.get(name = map_name)
    if not request.user.is_authenticated:
        return_data = {
        "data_type": "Map_reqeust_response",
        "data": {
            "map_name": map_name,
            "edge": map.edges,
            "node": map.node,
            "map_description": map.map_description
        }
    }
    else:
        user = authmodels.user.objects.get(uid = request.user.username)
        update_user_history(user, map_name)
        return_data = {
            "data_type": "Map_reqeust_response",
            "data": {
                "map_name": map_name,
                "map_manager": map.manager,
                "map_editor": map.editor,
                "edge": map.edges,
                "node": map.node,
                "map_description": map.map_description
            }
        }
    print(return_data)
    print(request.session["uid"])
    return_data = json.dumps(return_data)
    return JsonResponse(return_data, safe = False, status = 200)

# {map_name, user}
@login_required
@require_http_methods(['PUT'])
def grant_edit_permission(request):
    # the request is the map_manager of that specific map
    # update the map's editor entry to add the user
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            datatype = data["update_editor"]
            if datatype != "Map_update":
                raise json.JSONDecodeError
            data = data["data"]
            map_name = data["map_name"]
            map_editor = data["map_editor"] # should be a list of updated editors, not just the new editor
        except json.JSONDecodeError:
            return HttpResponse("key error", status = 400)
    else :
        return HttpResponse("Wrong data content type, only accept json\n",status = 400)
    # check permission
    map = models.map.objects.get(name = map_name)
    map_manager = map.manager
    user = authmodels.user.objects.get(uid = request.user.username)
    if user.username not in map_manager:
        return HttpResponse("Permission denied\n",status = 403)
    
    # update map
    map.editor = map_editor
    return HttpResponse("Success\n", status = 200)
    
# temparary create map for dev stage.
@require_http_methods(['POST'])
def dev_create_map(request):
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied\n",status = 403)
    data = request.body
    # parse data
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            datatype = data["data_type"]
            if datatype != "Map":
                raise json.JSONDecodeError
            data = data["data"]
            map_name = data["map_name"]
            map_description = data["map_description"]
            map_editor = data["map_editor"]
            map_manager = data["map_manager"]
            map_edge = data["map_edge"]
            map_node = data["map_node"]
        except json.JSONDecodeError:
            return HttpResponse("key error", status = 400)
    else :
        return HttpResponse("Wrong data content type, only accept json\n",status = 400)
    # create new map entry in database
    try:
        models.map.objects.create(name = map_name, editor = map_editor, manager = map_manager, edges = map_edge, node = map_node, map_description = map_description)
    except IntegrityError as e:
        return HttpResponse( e + "Map with that name already exists\n",status = 400)

@login_required
@require_http_methods(['DELETE'])
# should be manager only, not sure if dev need to manually verify
def delete_map(request):
    #--todo--
    pass

# Since user can't create map before we manually verify them, the actual map creation probably can't be done directly by the user, this would be more of a notification to the devs?
def create_map(request):
    pass

@login_required
@require_http_methods(['PUT'])
def update_map(request):
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            datatype = data["data_type"]
            if datatype != "Map_update":
                raise json.JSONDecodeError
            data = data["data"]
            map_name = data["map_name"]
            map_description = data["map_description"]
            map_edge = data["map_edge"]
            map_node = data["map_node"]
        except json.JSONDecodeError:
            return HttpResponse("key error", status = 400)
    else :
        return HttpResponse("Wrong data content type, only accept json\n",status = 400)
    
    # check permission
    map = models.map.objects.get(name = map_name)
    if request.user.username not in map.editor or request.user.username not in map.manager:
        return HttpResponse("Permission denied\n",status = 403)
    # update map
    map.map_description = map_description
    map.edges = map_edge
    map.node = map_node
    map.save()
    return HttpResponse("Success\n", status = 200)
    
    
# return user information all at once 
def get_user_info(request):
    if not request.user.is_authenticated:
        return HttpResponse("Permission denied\n",status = 403)
    uid = request.session["uid"]
    user = models.map.objects.filter(uid = request.user.username)
    username = user.username
    managed_map = user.managed_map
    editable_map = user.editable_map
    history = user.history
    
    # craft return json
    data = {
        "data_type": "User",
        "data":{
            "uid": uid,
            "Username": username,
            "managed_map": managed_map,
            "editable_map": editable_map,
            "history": history
        }
    }
    # return in json
    data = json.dumps(data)
    return JsonResponse(data, status = 200)






# old structure -----------------------------------
@csrf_exempt
@login_required
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
                update_data = data["map_description"]
                print(query_map)
                print(update_data)
            except json.JSONDecodeError:
                return HttpResponse("key error", status = 400)
        else :
            print("not json data")
        print(user.username)
        permission = authmodels.userPermission.objects.get(uid = user.username)
        if permission == None or permission.level < 2:
            return HttpResponse("Permission denied: No edit permission\n",status = 403)
        else:
            if models.map_editor.objects.filter(uid = user.username, map = query_map).exists():
                map = models.map_description.objects.get(map = query_map)
                map.map_description = update_data
                map.save()
                return HttpResponse("success\n", status = 200)
            else:
                message = "Permission denied: No '" + query_map + "' edit rights\n"
                return HttpResponse(message,status = 403)
    else:
        return HttpResponse("Permission denied\n",status = 403)
    
    