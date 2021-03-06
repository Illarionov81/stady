from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from api_v2.permissions import GetModelPermissions
from api_v2.serializers import ArticleSerializers, UserSerializer
from webapp.models import Article


class UserDetail(ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ArticleViewSet(ViewSet):
    queryset = Article.objects.all()
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [GetModelPermissions()]
        else:
            return [AllowAny()]

    def list(self, request):
        objects = Article.objects.all()
        slr = ArticleSerializers(objects, many=True, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        slr = ArticleSerializers(data=request.data, context={'request': request})
        if slr.is_valid():
            article = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        slr = ArticleSerializers(article, context={'request': request})
        return Response(slr.data)

    def update(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        slr = ArticleSerializers(data=request.data, instance=article, context={'request': request})
        if slr.is_valid():
            article = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def destroy(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({'pk': pk})
