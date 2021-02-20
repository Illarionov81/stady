from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api_v2.views import ArticleViewSet

app_name = 'api_v2'

router = DefaultRouter()
router.register(r'article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls))
]