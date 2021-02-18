from django.contrib.auth import get_user_model

from accounts.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms


class XDatepickerWidget(forms.TextInput):
    template_name = 'widgets/xdatapicr.html'


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        field_classes = {'username': UsernameField}


class UserChangeForm(forms.ModelForm):
    birth_date = forms.DateTimeField(required=False, label='Время публикации', input_formats=['%Y-%m-%d', '%d.%m.%Y'],
                                     widget=XDatepickerWidget)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'avatar']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email', 'birth_date': 'дата рождения',
                  'avatar': 'аватарка'}


# class PasswordChangeForm(forms.ModelForm):
#     password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
#     password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
#     old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)
#
#     def clean_password_confirm(self):
#         password = self.cleaned_data.get("password")
#         password_confirm = self.cleaned_data.get("password_confirm")
#         if password and password_confirm and password != password_confirm:
#             raise forms.ValidationError('Пароли не совпадают!')
#         return password_confirm
#
#     def clean_old_password(self):
#         old_password = self.cleaned_data.get('old_password')
#         if not self.instance.check_password(old_password):
#             raise forms.ValidationError('Старый пароль неправильный!')
#         return old_password
#
#     def save(self, commit=True):
#         user = self.instance
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user
#
#     class Meta:
#         model = get_user_model()
#         fields = ['password', 'password_confirm', 'old_password']