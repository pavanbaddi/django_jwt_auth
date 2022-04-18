from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class JwtTokenModel(models.Model):
    token_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, related_name="auth_tokens", on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=datetime.datetime.now(), null=True)
    updated_at = models.DateTimeField(auto_now_add=datetime.datetime.now(), null=True)

    class Meta():
        db_table = "auth_tokens"


    # def get_or_create(self, **kwargs )