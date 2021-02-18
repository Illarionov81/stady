from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User
from main.settings import AUTH_USER_MODEL


def _(param):
    pass


class MyUserInline(UserAdmin):
    # model = get_user_model()
    exclude = []
    list_display = ['image_img', "username", 'birth_date', ]
    readonly_fields = ['image_img', ]
    list_display_links = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'image_img', 'birth_date',)}),
    )


# class ProfileAdmin(UserAdmin):
#     inlines = [MyUserInline]


admin.site.register(User, MyUserInline)
