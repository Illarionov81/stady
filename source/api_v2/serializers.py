from django.contrib.auth import get_user_model
from rest_framework import serializers
from webapp.models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='api_v2:user-detail')
    articles_url = serializers.HyperlinkedRelatedField(many=True, read_only=True, source='articles',
                                                       view_name='api_v2:article-detail')

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'url', 'first_name', 'last_name', 'email', 'articles_url']


class ArticleSerializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='api_v2:article-detail')
    author_url = serializers.HyperlinkedRelatedField(read_only=True, source='author',
                                                     view_name='api_v2:user-detail')
    author = UserSerializer(read_only=True)
    tags_display = TagSerializer(many=True, read_only=True, source='tags')

    class Meta:
        model = Article
        fields = ['id', 'url', 'title', 'text', 'author', 'author_url', 'status',
                  'created_at', 'updated_at', 'tags', 'tags_display']
        read_only_fields = ('author',)
