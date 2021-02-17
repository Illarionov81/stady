from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from main.settings import AUTH_USER_MODEL


class MyUserInline(admin.ModelAdmin):
    model = AUTH_USER_MODEL
    exclude = []
    # list_display = ['birth_date', 'pk']


admin.site.register(User, MyUserInline)
# admin.site.register(User, UserAdmin)
