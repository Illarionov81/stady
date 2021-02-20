from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api_v2.serializers import ArticleSerializers
from webapp.models import Article


class ArticleViewSet(ViewSet):
    queryset = Article.objects.all()

    def list(self, request):
        objects = Article.objects.all()
        slr = ArticleSerializers(objects, many=True)
        return Response(slr.data)

    def create(self, request):
        slr = ArticleSerializers(data=request.data)
        if slr.is_valid():
            article = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        slr = ArticleSerializers(article)
        return Response(slr.data)

    def update(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        slr = ArticleSerializers(data=request.data, instance=article )
        if slr.is_valid():
            article = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def destroy(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({'pk': pk})
