from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.base import View, TemplateView
from django.utils.timezone import make_naive

from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT
from webapp.models import Article


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        data = Article.objects.all()
        is_admin = self.request.GET.get('is_admin', None)
        if not is_admin:
            data = data.filter(status='moderated')
        search = self.request.GET.get('search')
        if search:
            data = data.filter(title__icontains=search)
        return data.order_by('-created_at')


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(Article, pk=kwargs['pk'])
        return context


class ArticleCreateView(View):
    def get(self, request):
        form = ArticleForm()
        return render(request, 'article_create.html', context={'form': form})

    def post(self, request):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            data = {}
            tags = form.cleaned_data.pop('tags')
            for key, value in form.cleaned_data.items():
                if value is not None:
                    data[key] = value
            article = Article.objects.create(**data)
            article.tags.set(tags)
            return redirect('article', pk=article.pk)
        else:
            return render(request, 'article_create.html', context={'form': form})


class ArticleUpdateView(TemplateView):
    template_name = 'update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        initial = {}
        for key in 'title', 'text', 'author', 'status':
            initial[key] = getattr(article, key)
        initial['publish_at'] = make_naive(article.publish_at).strftime(BROWSER_DATETIME_FORMAT)
        initial['tags'] = article.tags.all()
        form = ArticleForm(initial=initial)
        context['form'] = form
        context['article'] = article
        return context

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            tags = form.cleaned_data.pop('tags')
            for key, value in form.cleaned_data.items():
                if value is not None:
                    setattr(article, key, value)
            article.save()
            article.tags.set(tags)
            return redirect('article', pk=article.pk)
        else:
            return self.render_to_response({'form': form, 'article': article})


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', context={'article': article})
    elif request.method == 'POST':
        article.delete()
        return redirect('index')
