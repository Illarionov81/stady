from django.urls import path

from api_1.views import json_echo_view, get_token_view, ArticleCreateView, ArticleListView

app_name = 'api_1'

urlpatterns = [
    path('echo/', json_echo_view),
    path('get-token/', get_token_view),
    path('article-create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
]