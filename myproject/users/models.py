from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
import secrets

class OtpToken(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="otps")
    otp = models.CharField(max_length=6,default=secrets.token_hex(3))
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return f"OTP for {self.user.username}: {self.otp}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username