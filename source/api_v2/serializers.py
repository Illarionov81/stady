from rest_framework import serializers
from webapp.models import Article


class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'author', 'status', 'created_at', 'updated_at']
        read_only_fields = ('author',)
