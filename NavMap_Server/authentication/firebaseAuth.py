from firebase_admin import auth
from functools import wraps
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User, AnonymousUser
from .models import userPermission
# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("./credentials.json")
# firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except auth.InvalidIdTokenError:
        return None

# only for testing
def get_userInfo(jwt):
    # parse uid to get jwt
    
    #check if uid is in the database
    print(jwt)
    if jwt == None:
        return None
    if userPermission.objects.filter(uid=jwt):
        print(userPermission.objects.get(uid=jwt).level)
        return userPermission.objects.get(uid=jwt).uid
    return None

class firebaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    
    def process_request(self, request):
        print("request processing by middleware")
        jwt = request.headers.get('Authorization')
        if jwt == None:
            #then it will create a anonymous user
            request.user= AnonymousUser()
            pass
        else:
            jwt = jwt.split(' ')
            jwt = jwt[1]
            # uid = verify_firebase_token(jwt)
            user,created = User.objects.get_or_create(username = jwt)
            request.user = user
            get_userInfo(jwt)
        #check uid with the database
        
    
    def process_response(self, request, response):
        print("response goes through middleware")
        
    def process_exception(self, request, exception):
        print("excption")
    