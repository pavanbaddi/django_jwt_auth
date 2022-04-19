from django.contrib.auth.models import User

from login.models import JwtTokenModel
from django.contrib.auth.models import AnonymousUser

from login.views import is_external_request
from zoneinfo import ZoneInfo

class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # def __call__(self, request):
    #     response = self.process_request(request)
    #     if response is None:
    #         response = self.get_response(request)
    #     return response

    def __call__(self, request):
        excluded_paths = ['/verify']

        if request.path not in excluded_paths:
            upgraded_request, token, expiry_datetime, token_updated = self.process_request(request)
            response = self.get_response(upgraded_request)
            if token_updated:
                response.set_cookie(key="token", value=token, expires=expiry_datetime)
        else:
            response = self.get_response(request)
        return response

    def process_request(self, request):
        user = request.user
        token = request.COOKIES.get("token")
        expiry_datetime = None
        updated = False
        if token:
            token_object = JwtTokenModel.objects.filter(token=token).first()
            token_object, updated = token_object.renew()
            if updated:
                token = token_object.token
                request.COOKIES.update({"token" : token})
                expiry_datetime = token_object.expiry_datetime.astimezone(ZoneInfo("Asia/Kolkata")).strftime("%a, %d %b %Y %H:%M:%S %Z")
                print("process requet", expiry_datetime)
            
            user = token_object.user if token_object else AnonymousUser()

        request.user = user

        return request, token, expiry_datetime, updated