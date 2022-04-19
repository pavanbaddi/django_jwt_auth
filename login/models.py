from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from zoneinfo import ZoneInfo
import pytz
# Create your models here.
class JwtTokenModel(models.Model):
    token_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, related_name="auth_tokens", on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiry_datetime = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now_add=datetime.datetime.now(), null=True)

    class Meta():
        db_table = "auth_tokens"

    def is_expired(self):
        expiry_datetime = self.expiry_datetime
        now = datetime.datetime.now(tz=ZoneInfo("Asia/Kolkata"))
        return now >= expiry_datetime

    def renew(self):
        updated = False
        token = self
        has_expired = self.is_expired()
        print("has_expired", has_expired)
        if has_expired:
            from login.views import jwt_encode
            updated = True
            now = datetime.datetime.now(tz=ZoneInfo("Asia/Kolkata"))
            additional_time = datetime.timedelta(minutes=1)
            expiry_datetime = now+additional_time
            self.token = jwt_encode({
                "id" : self.user.pk,
                "username" : self.user.username,
                "email" : self.user.email,
                "expiry_datetime" : expiry_datetime.strftime("%a, %d %b %Y %H:%M:%S %Z")
            })
            self.expiry_datetime = expiry_datetime
            self.save()

            token = self

        return token, updated


    # def get_or_create(self, **kwargs )