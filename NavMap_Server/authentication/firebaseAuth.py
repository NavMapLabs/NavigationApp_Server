from firebase_admin import auth
from functools import wraps
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.models import Session
from .models import user
import firebase_admin, os
from firebase_admin import credentials
from NavMap_Server import settings

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cred = credentials.Certificate(os.path.join(BASEDIR, "authentication/firebase_credentials.json"))
firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['user_id']
        
        return uid
    except auth.InvalidIdTokenError:
        print("exception bitch")
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
        # make sure the admin page can still work properly in browser, need to fix when we need admin to remotely grant access through http request
        # for now using the webpage built-in page can work.
        if "admin" in request.path:
            return
        
        
        if settings.DEBUG:
            print(f'debug mode is on: current user{request.user}')
            # if auth session exist, skip the firebase validation and use the session to update user object
            # ============= session ===============
            if "login_user" in request.user.username:
                request.session["uid"] = request.user.username
                return 
        else:
            if request.session.session_key and request.session.exists(request.session.session_key):
                # --todo: fetch the session key
                print("has session")
                if 'uid' not in request.session:
                    request.user = AnonymousUser()
                    return
                uid = request.session.get("uid")
                # --todo: set the user object to the user with sesseion value username
                user,created = User.objects.get_or_create(username = uid)
                request.user = user
                return
        
        jwt = request.headers.get('Authorization')
        if jwt == None or jwt == "":
            request.user = AnonymousUser()
            pass
        else:
            jwt = jwt.split(' ')
            jwt = jwt[1]
            # uid = verify_firebase_token(jwt)
            uid = jwt
            if uid == None:
                request.user = AnonymousUser()
                return
            #right now it stores user_id as username.
            user,created = User.objects.get_or_create(username = uid)
            request.user = user
            
            #--todo:store username in session dictionary for the first time session is created
            request.session["uid"] = uid
        # check uid with the database for previlege?

        
    
        
    
    def process_response(self, request, response):
        # print("response goes through middleware")
        pass
        
    def process_exception(self, request, exception):
        print("excption")
    