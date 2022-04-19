from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.forms.models import model_to_dict
from login.models import JwtTokenModel
import jwt
import json
import datetime
from zoneinfo import ZoneInfo

# Create your views here.
def index(request):
    return render(request, 'login/login.html')

def dashboard(request):

    is_external = is_external_request(request)
    # print("dashboard", request.user.id)
    if is_external:
        print("dashboard request.user: ", request.user)
        if request.user.is_authenticated:
            return JsonResponse(data=model_to_dict(request.user))
        
        return JsonResponse(status=403, data={
            "message" : "User not valid"
        })
    return render(request, 'login/dashboard.html')
    
def user_logout(request):
    logout(request)
    return redirect(reverse("login:index"))

@csrf_exempt
def login_verify(request):
    # print(json.loads(request.body))
    # return ""
    username = request.POST["username"]
    password = request.POST["password"]
    
    user = authenticate(request, username=username, password=password)
    is_external = is_external_request(request)
    if user is not None:
        if is_external:
            now = datetime.datetime.now(tz=ZoneInfo("Asia/Kolkata"))
            additional_time = datetime.timedelta(minutes=1)
            expiry_datetime = now+additional_time
            token_object = JwtTokenModel.objects.filter(user=user).order_by('-token_id').first()
            # generate token
            if token_object is None:
                token_object = JwtTokenModel.objects.create(**{
                    "user" : user,
                    "token" : jwt_encode({
                        "id" : user.pk,
                        "username" : user.username,
                        "email" : user.email,
                        "expiry_datetime" : expiry_datetime.strftime("%a, %d %b %Y %H:%M:%S %Z")
                    }),
                    "expiry_datetime" : expiry_datetime
                })

            if token_object.expiry_datetime is None:
                token_object.expiry_datetime = expiry_datetime
                token_object.save()

            response = JsonResponse(data={"success" : True})
            expires = token_object.expiry_datetime.astimezone(ZoneInfo("Asia/Kolkata")).strftime("%a, %d %b %Y %H:%M:%S %Z")
            print("expires", expires)
            response.set_cookie(key="token", value=token_object.token, expires=expires)
            # return JsonResponse(data={"success" : True, "token" : token_object.token})
            return response
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