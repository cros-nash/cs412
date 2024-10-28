from django.contrib import admin
# Register your models here.
from .models import Friend, Profile, StatusMessage, Image
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)