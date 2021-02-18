from django.shortcuts import render

import json
from datetime import datetime
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    else:
        return HttpResponseNotAllowed("Only GET response are allowed")


def json_echo_view(request, *args, **kwargs):
    answer = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'method': request.method
    }
    if request.method == 'POST':
        data = json.loads(request.body)
        answer['data'] = data
    return JsonResponse(answer)


class ArticleCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        article = Article.objects.create(**data)
        # article = Article.objects.create(
        #     author_id=data['author_id'],
        #     title=data['title'],
        #     text=data['text']
        # )
        return JsonResponse({
            'pk': article.pk,
            'author_id': article.author_id,
            'title': article.title,
            'text': article.text,
            'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': article.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        })