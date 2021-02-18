from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import MyUserCreationForm, UserChangeForm
from accounts.models import User


class RegisterView(CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        articles = self.object.articles.order_by('-created_at')
        paginator = Paginator(articles, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['articles'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    context_object_name = 'user_obj'
    template_name = 'user_change.html'

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})
