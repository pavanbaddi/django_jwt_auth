from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class AuthUserBackend:
	
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
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None