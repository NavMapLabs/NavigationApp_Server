from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
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
    authmodels.user.objects.create(uid = request.user.username, user_name = request.user.username, permission_level = 1)
    return
# ---------------------------------- end of helper function -----------------------------------

# return the maps that match with the search, no auth needed
@require_http_methods(['GET'])
#input map name, return map_id
def search(request):
    # return the list of matched map name (maybe the description)
    #--todo -------
    pass


# return the edge and node data to the frontend, no auth needed
@csrf_exempt
@require_http_methods(['GET'])
#input map name return map information and all variations
def get_map_meta_info(request):
    create_user_entry(request)
    map_name = request.GET.get('param1')
    print(map_name)
    if map_name == None:
        return HttpResponse("parameter error", status = 400)
    # get data
    try:
        map = models.maps.objects.get(map_name = map_name)
        map_variations = models.map_variation.objects.filter(map_info__map_name = map_name)
    except models.maps.DoesNotExist:
        return HttpResponse("map not found\n", status = 404)
    variations_maps_dict = dict()
    
    if not map_variations.exists():
        return HttpResponse("no map variation found, which shouldn't happen, please contact devs\n", status = 404)
    count = 0
    for variation in map_variations:
        count += 1
        map_variation_data = dict()
        map_variation_data["version_name"] = variation.version_name
        map_variation_data["map_id"] = str(variation.map_id)
        map_variation_data["map_editor"] = variation.map_editor.user_name
        variations_maps_dict[count] = map_variation_data
        
    
    data = dict()
    return_data = dict()
    data["variations_count"] = count
    data["map_name"] = map_name
    data["map_addr"] = map.map_addr
    data["map_description"] = map.map_description
    data["variations"] = variations_maps_dict
    return_data["data"] = data
    # return_data = json.dumps(return_data)
    print(return_data)
    print(request.session["uid"])
    return JsonResponse(return_data, status = 200)

# for later
@login_required
@require_http_methods(['PUT'])
def grant_edit_permission(request):
    pass


@csrf_exempt
@require_http_methods(['GET'])
def id_to_data(request):
    create_user_entry(request)
    map_id = request.GET.get('param1')
    if map_id == None:
        return HttpResponse("parameter error", status = 400)
    try:
        map_variation = models.map_variation.objects.get(map_id = map_id)
    except models.map_variation.DoesNotExist:
        return HttpResponse("map not found\n", status = 404)
    data = dict()
    data["map_id"] = map_id
    data["map_data"] = map_variation.map_data
    data["version_name"] = map_variation.version_name
    data["map_editor"] = map_variation.map_editor.user_name
    return JsonResponse(data, status = 200)

# temparary create map for dev stage.
@csrf_exempt
@login_required
@require_http_methods(['POST'])
def dev_create_map(request):
    create_user_entry(request)
    uid = request.session.get('uid')
    user = authmodels.user.objects.get(uid = uid)
    if not request.user.is_authenticated and uid == None:
        return HttpResponse("Permission denied\n",status = 403)
    #check permission/ get session uid
    if user.permission_level < 2:
        return HttpResponse("need to go through admin page to pump you permission to editor manually for now\n",status = 403)
    
    data = request.body
    # parse data
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            data = data["data"]
            # it need map name, map addr, map data
            map_name = data["map_name"]
            version_name = data["version_name"]
            map_address = data["map_address"]
            map_data = data["map_data"]
        except (json.JSONDecodeError, KeyError, TypeError):
            return HttpResponse("key error", status = 500)
    else :
        return HttpResponse("Wrong data content type, only accept json\n",status = 400)
    # check for optional fields
    map_description = ""
    if 'map_description' in data:
        map_description = data["map_description"]
    # create new map entry in database
    if models.maps.objects.filter(map_name = map_name).exists():
        return HttpResponse("Map with that name already exists\n",status = 400)
    try:
        models.maps.objects.create(map_name= map_name, map_addr = map_address, map_description = map_description)
        new_map= models.maps.objects.get(map_name = map_name)
        models.map_variation.objects.create(version_name = version_name, map_info = new_map, map_editor = user, map_data = map_data)
    except IntegrityError as e:
        # so if map with the same name already exist, or variation with the same map_id already exist
        models.maps.objects.get(map_name = map_name).delete()
        return HttpResponse( "can't make variation object\n",status = 400)
    return HttpResponse("Success\n", status = 200)

@csrf_exempt
@login_required
@require_http_methods(['DELETE'])
# should be manager only, not sure if dev need to manually verify
def delete_map(request):
    create_user_entry(request)
    uid = request.session.get('uid')
    user = authmodels.user.objects.get(uid = uid)
    if not request.user.is_authenticated and uid == None:
        return HttpResponse("Permission denied\n",status = 403)
    #check permission/ get session uid
    if user.permission_level < 2:
        return HttpResponse("need to go through admin page to pump you permission to editor manually for now\n",status = 403)
    
    # get the map_id from the map_version you want to delete, not sure if putting it in parameter is safe
    create_user_entry(request)
    map_id= request.GET.get('param1').lower()
    print(map_id)
    if map_id == None:
        return HttpResponse("parameter error", status = 400)
    
    
    
    # data = request.body
    # # parse data
    # if request.content_type == 'application/json':
    #     try:
    #         data = json.loads(request.body)
    #         datatype = data["data_type"]
    #         if datatype != "Map_update":
    #             raise json.JSONDecodeError
    #         data = data["data"]
    #         # it need map name, map addr, map data
    #         map_id = data["map_id"]
    #     except (json.JSONDecodeError, KeyError):
    #         return HttpResponse("key error", status = 400)
    # else :
    #     return HttpResponse("Wrong data content type, only accept json\n",status = 400)
    # # need to update this later
    try:
        #check if it's still exist
        map_varient = models.map_variation.objects.get(map_id = map_id)
        # check if it's the only version, if it is, delete the map as well
        print(models.map_variation.objects.filter(map_info = map_varient.map_info).count())
        models.map_variation.objects.get(map_id = map_id).delete()
        print(models.map_variation.objects.filter(map_info = map_varient.map_info).count())
        if models.map_variation.objects.filter(map_info = map_varient.map_info).count() == 0:
            print("count is 0")
            map_varient.map_info.delete()
    except :
        return HttpResponse("map varient does not exist\n",status = 400)
    return HttpResponse("Success\n", status = 200)

# Since user can't create map before we manually verify them, the actual map creation probably can't be done directly by the user, this would be more of a notification to the devs?
def create_map(request):
    pass

# use case, update on existing variation, update on new variation 
@csrf_exempt
@login_required
@require_http_methods(['PUT'])
def update_map(request):
    create_user_entry(request)
    uid = request.session.get('uid')
    user = authmodels.user.objects.get(uid = uid)
    if not request.user.is_authenticated and uid == None:
        return HttpResponse("Permission denied\n",status = 403)
    #check permission/ get session uid
    if user.permission_level < 2:
        return HttpResponse("need to go through admin page to pump you permission to editor manually for now\n",status = 403)
    data = request.body
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            data = data["data"]
            map_name = data["map_name"]
            version_name = data["version_name"]
            map_data = data["map_data"] 

        except json.JSONDecodeError:
            return HttpResponse("key error", status = 400)
    else :
        return HttpResponse("Wrong data content type, only accept json\n",status = 400)

    # check if map exist
    try:        
        maps = models.maps.objects.get(map_name = map_name)
        if "map_description" in data:
            maps.map_description = data["map_description"]
        # create new map variation
        
        if not "map_id" in data :
            model = models.map_variation.objects.create(version_name = version_name, map_info = maps, map_editor = user, map_data = map_data)
            id = model.map_id
            message = "sucess, New map id:\n" + str(id)
            return HttpResponse(message,status = 200)
        # update the old variation
        else:
            
            map_varient = models.map_variation.objects.get(map_id = data["map_id"])
            map_varient.map_data = map_data
            map_varient.version_name = version_name
            map_varient.save()
            return HttpResponse("sucess\n",status = 200)          
    except (models.maps.DoesNotExist, models.map_variation.DoesNotExist , ValidationError) :
        return HttpResponse("map not found\n", status = 404)  
    
    
# return user information all at once 
def get_user_info(request):
    pass

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
    
    