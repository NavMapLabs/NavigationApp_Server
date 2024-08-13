from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from authApp.decorators import role_required
import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings

firebase_creds = credentials.Certificate(settings.FIREBASE_CONFIG)
firebase_app = firebase_admin.initialize_app(firebase_creds)

# Create your views here.
def home(request):
    return HttpResponse("Hello, Welcome to the Homepage")

@role_required('admin')
def admin_view(request):
    # Access user information
    user = request.user
    context = {
        'username': user.username,
        'role': user.role,
    }
    return render(request, 'authApp/admin_view.html', context)

def getData(request):
    # get token
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    token = authorization_header.replace("Bearer ", "")
    
    # verify the token
    try:
        decoded_token = auth.verify_id_token(token)
        firebase_user_id = decoded_token['user_id'] # got from checking jwt token from jwt.io
        data = {
            "message": "Hello, this is a JSON response!",
            "status": "success",
            "data": {
                "id": 1,
                "name": "Sample Item",
                "description": "This is a sample description."
            }
        }
    except:
        return JsonResponse({"data": "user token is invalid"})
    
    # Return the data as a JSON response
    return JsonResponse(data)