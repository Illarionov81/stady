from django import forms
from django.forms import widgets

from webapp.models import Tag, Article, STATUS_CHOICES

default_status = STATUS_CHOICES[0][0]
BROWSER_DATETIME_FORMAT = '%Y-%m-%dT%H:%M'


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Title')
    author = forms.CharField(max_length=40, required=True, label='Author')
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial=default_status, label='Модерация')
    text = forms.CharField(max_length=3000, required=True, label='Text', widget=widgets.Textarea)
    tags = forms.ModelMultipleChoiceField(required=False, label="Тэги", queryset=Tag.objects.all())
    publish_at = forms.DateTimeField(required=False, label='Время публикации',
                                     input_formats=['%Y-%m-%d', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S',
                                                    '%Y-%m-%dT%H:%M:%S', BROWSER_DATETIME_FORMAT],
                                     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Статья')
