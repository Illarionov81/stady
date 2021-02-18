from django.urls import path

from api_1.views import json_echo_view

app_name = 'api_1'

urlpatterns = [
    path('echo', json_echo_view)
]