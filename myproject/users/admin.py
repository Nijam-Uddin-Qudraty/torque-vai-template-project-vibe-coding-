from django.contrib import admin

# Register your models here.
from .models import UserProfile
admin.site.register(UserProfile)
list_display = ('user', 'bio', 'location')
def user_profile(self, obj):
    return obj.user.username