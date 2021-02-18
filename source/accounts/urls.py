from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# from accounts.views import login_view, logout_view
from accounts.views import RegisterView, UserDetailView, UserChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign-up/', RegisterView.as_view(), name='sign_up'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', UserChangeView.as_view(), name='change')
]
