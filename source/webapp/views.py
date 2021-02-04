from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from webapp.models import Article


def index_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'index.html', context)


def article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article.html', context={'article': article})


def article_create_view(request):
    if request.method == 'GET':
        return render(request, 'article_create.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('content')
        author = request.POST.get('author')
        article = Article.objects.create(title=title, text=text, author=author)

        return redirect('article', pk=article.pk)
