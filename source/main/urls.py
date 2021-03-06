"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from webapp.views import IndexView, ArticleCreateView, ArticleView, ArticleUpdateView, ArticleDeleteView, \
    ArticleCommentCreateView, mass_article_delete, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api_1.urls')),
    path('api/v2/', include('api_v2.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', IndexView.as_view(), name='index'),
    path('articles/mass-delete/', mass_article_delete, name='article_mass_delete'),
    path('articles/add/', ArticleCreateView.as_view(), name='article_add'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArticleDeleteView.as_view(), name='article_delete'),

    path('article/<int:pk>/add-comment', ArticleCommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete'),

    path('accounts/', include('accounts.urls')),
    path('silk/', include('silk.urls', namespace='silk'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
