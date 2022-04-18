from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.forms.models import model_to_dict
from login.models import JwtTokenModel
import jwt

# Create your views here.
def index(request):
    return render(request, 'login/login.html')

def dashboard(request):
    # breakpoint()
    print("request from",  {
       "HTTP_CONTENT" : request.META.get("HTTP_CONTENT"),
       "REMOTE_ADDR" : request.META.get("REMOTE_ADDR"),
       "REMOTE_HOST" : request.META.get("REMOTE_HOST"),
       "HTTP_HOST" : request.META.get("HTTP_HOST"),
       "request.user.id" : request.user.id if request.user.is_authenticated else None,
    })
    is_external = is_external_request(request)
    # print("dashboard", request.user.id)
    if is_external:
        if request.user.is_authenticated:
            return JsonResponse(data=model_to_dict(request.user))
        
        return JsonResponse(data={
            "message" : "User not valid"
        })
    return render(request, 'login/dashboard.html')
    
def user_logout(request):
    logout(request)
    return redirect(reverse("login:index"))

@csrf_exempt
def login_verify(request):
    # breakpoint()
    username = request.POST["username"]
    password = request.POST["password"]

    print("request from",  {
       "HTTP_CONTENT" : request.META.get("HTTP_CONTENT"),
       "REMOTE_ADDR" : request.META.get("REMOTE_ADDR"),
       "REMOTE_HOST" : request.META.get("REMOTE_HOST"),
       "HTTP_HOST" : request.META.get("HTTP_HOST"),
       "username" : username,
       "password" : password,
    })
    
    

    user = authenticate(request, username=username, password=password)
    is_external = is_external_request(request)
    if user is not None:
        if is_external:
            # generate token
            token_object, created = JwtTokenModel.objects.get_or_create(
                user=user,
                defaults={
                    "user" : user,
                    "token" : jwt_encode({
                        "id" : user.pk,
                        "username" : user.username,
                        "email" : user.email,
                    })
                }
            )
            return JsonResponse(data={"success" : True, "token" : token_object.token})
        else:
            login(request, user)
            return redirect(reverse("login:dashboard"))
    else:
        return  redirect(reverse("login:index")) if is_external == False else JsonResponse(data={"success" : False})

    
def is_external_request(request):
    return True if request.META.get("HTTP_CONTENT") else False

def jwt_encode(payload):
    key = settings.JWT_SETTINGS["secret"]
    alg = settings.JWT_SETTINGS["alg"]
    token = jwt.encode(payload, key, algorithm=alg)   
    return token