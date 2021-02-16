from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.timezone import make_naive

from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT, SimpleSearchForm
from webapp.models import Article


def mass_article_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected', [])
        if 'delete' in request.POST:
            Article.objects.filter(id__in=ids).delete()
    return redirect('index')


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


class ArticleView(DetailView):
    template_name = 'articles/article.html'
    model = Article
    paginete_comments_by = 2
    paginete_comments_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        comments, page, is_paginated = self.paginater_comments(self.object)

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


class ArticleCreateView(CreateView):
    template_name = 'articles/article_create.html'
    model = Article
    form_class = ArticleForm

    def get_success_url(self):
        return reverse('article', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UpdateView):
    template_name = 'articles/update.html'
    model = Article
    form_class = ArticleForm

    def get_initial(self):
        return {'publish_at': make_naive(self.object.publish_at).strftime(BROWSER_DATETIME_FORMAT)}

    def get_success_url(self):
        return reverse('article', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    template_name = 'articles/delete.html'
    model = Article
    success_url = reverse_lazy('index')
