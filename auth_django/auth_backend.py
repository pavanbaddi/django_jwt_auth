from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend, ModelBackend
class AuthUserBackend(ModelBackend):
    def authenticate(self,request,username=None,password=None):
        if username and password:
            try:
                user = User.objects.get(username=username)
                if check_password(password,user.password):
                    if user.is_active:
                        return user
            except User.DoesNotExist:
                return None
        return None

    def get_user(self,user_id):
        print("get_user", user_id)
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None