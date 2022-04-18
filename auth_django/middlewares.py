from django.contrib.auth.models import User

from login.models import JwtTokenModel
from django.contrib.auth.models import AnonymousUser

from login.views import is_external_request

class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.process_request(request)
        if response is None:
            response = self.get_response(request)
        return response

    # def process_view(self,request, view_func, view_args, view_kwargs):
    #     # id = request.COOKIES.get('logged_in_id') 
    #     # return None
    #     breakpoint()
    #     print("entered")


    def process_request(self, request):
        print("process_request", request.user)
        # breakpoint()
        user = request.user

        if "bearer " in request.headers.get("Authorization", ""):
            token = request.headers["Authorization"].replace("bearer ", "")
            token = JwtTokenModel.objects.filter(token=token).first()
            user = token.user if token else AnonymousUser()
        request.user = user