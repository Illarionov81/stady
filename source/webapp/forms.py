from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Tag, Article, STATUS_CHOICES

default_status = STATUS_CHOICES[0][0]
BROWSER_DATETIME_FORMAT = '%Y-%m-%dT%H:%M'


def at_least_10(string):
    if len(string) < 10:
        raise ValidationError('This value is too short!')


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Title', validators=[at_least_10])
    author = forms.CharField(max_length=40, required=True, label='Author')
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial=default_status, label='Модерация')
    text = forms.CharField(max_length=3000, required=True, label='Text', widget=widgets.Textarea)
    tags = forms.ModelMultipleChoiceField(required=False, label="Тэги", queryset=Tag.objects.all())
    publish_at = forms.DateTimeField(required=False, label='Время публикации',
                                     input_formats=['%Y-%m-%d', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S',
                                                    '%Y-%m-%dT%H:%M:%S', BROWSER_DATETIME_FORMAT],
                                     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        text = cleaned_data.get('text')
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        if text and title and text == title:
            errors.append(ValidationError("Text of the article should not duplicate it's title!"))
        if title and author and title == author:
            errors.append(ValidationError("You should not write about yourself! It's a spam!"))
        if errors:
            raise ValidationError(errors)
        return cleaned_data


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Статья')
