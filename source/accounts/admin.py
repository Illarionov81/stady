from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User
from main.settings import AUTH_USER_MODEL


class MyUserInline(admin.ModelAdmin):
    model = AUTH_USER_MODEL
    exclude = []
    list_display = ['image_img', "username", 'birth_date', 'pk']
    readonly_fields = ['image_img', ]
    list_display_links = ['username']


admin.site.register(User, MyUserInline)
