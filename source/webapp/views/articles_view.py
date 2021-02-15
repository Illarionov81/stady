from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.base import View, TemplateView
from django.utils.timezone import make_naive

from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT, SimpleSearchForm
from webapp.models import Article


class IndexView(ListView):
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    paginate_by = 5
    paginate_orphans = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Article.objects.all()
        is_admin = self.request.GET.get('is_admin', None)
        if not is_admin:
            data = data.filter(status='moderated')
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(title__icontains=search) | Q(author__icontains=search))
        return data.order_by('-created_at')


class ArticleView(TemplateView):
    template_name = 'articles/article.html'
    paginete_comments_by = 2
    paginete_comments_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=kwargs['pk'])
        comments, page, is_paginated = self.paginater_comments(article)

        context['article'] = article
        context['comments'] = comments
        context['page_obj'] = page
        context['is_paginated'] = is_paginated
        return context

    def paginater_comments(self, article):
        comments = article.comments.all().order_by('-created_at')
        if comments.count() > 0:
            paginator = Paginator(comments, self.paginete_comments_by, orphans=self.paginete_comments_orphans)
            page = paginator.get_page(self.request.GET.get('page', 1))
            is_paginated = paginator.num_pages > 1
            return page.object_list, page, is_paginated
        return comments, None, False


class ArticleCreateView(View):
    def get(self, request):
        form = ArticleForm()
        return render(request, 'articles/article_create.html', context={'form': form})

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
            return render(request, 'articles/article_create.html', context={'form': form})


class ArticleUpdateView(TemplateView):
    template_name = 'articles/update.html'

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
        return render(request, 'articles/delete.html', context={'article': article})
    elif request.method == 'POST':
        article.delete()
        return redirect('index')
