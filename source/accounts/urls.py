from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# from accounts.views import login_view, logout_view
from accounts.views import register_view

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign-up/', register_view, name='sign_up')
]
