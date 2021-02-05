from django import forms
from django.forms import widgets

from webapp.models import Tag, Article, STATUS_CHOICES

default_status = STATUS_CHOICES[0][0]


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Title')
    author = forms.CharField(max_length=40, required=True, label='Author')
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial=default_status, label='Модерация')
    text = forms.CharField(max_length=3000, required=True, label='Text', widget=widgets.Textarea)
    tags = forms.ModelMultipleChoiceField(required=False, label="Таги", queryset=Tag.objects.all())


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Статья')
