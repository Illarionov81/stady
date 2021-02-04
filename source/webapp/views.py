from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View, TemplateView

from webapp.forms import ArticleForm
from webapp.models import Article


class IndexView(View):
    def get(self, request, *args, **kwargs):
        is_admin = self.request.GET.get('is_admin', None)
        if is_admin:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(status='moderated')
        context = {
            'articles': articles
        }
        return render(request, 'index.html', context)


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=kwargs['pk'])
        return context


def article_create_view(request, *args, **kwargs):
    if request.method == 'GET':
        form = ArticleForm()
        return render(request, 'article_create.html', context={'form': form})
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                status=form.cleaned_data['status']
            )
            tags=form.cleaned_data['tags']
            article.tags.set(tags)
            return redirect('article', pk=article.pk)
        else:
            return render(request, 'article_create.html', context={'form': form})


def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        form = ArticleForm(initial={
            'title': article.title,
            'text': article.text,
            'author': article.author
        })
        return render(request, 'update.html', context={'form': form, 'article': article})
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
            article.save()
            return redirect('article', pk=article.pk)
        else:
            return render(request, 'update.html', context={'form': form, 'article': article})


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', context={'article': article})
    elif request.method == 'POST':
        article.delete()
        return redirect('index')
