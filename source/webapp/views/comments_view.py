from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from webapp.forms import ArticleCommentForm
from webapp.models import Comment, Article


class ArticleCommentCreateView(CreateView):
    template_name = 'comments/comment_create.html'
    model = Comment
    form_class = ArticleCommentForm

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.article = article
        comment.author = self.request.user
        comment.save()
        return redirect('article', pk=article.pk)


class CommentUpdateView(UpdateView):
    template_name = 'comments/comment_update.html'
    model = Comment
    form_class = ArticleCommentForm

    def get_success_url(self):
        return reverse('article', kwargs={'pk': self.object.article.pk})


class CommentDeleteView(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('article', kwargs={'pk': self.object.article.pk})
