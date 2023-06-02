from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from .forms import *
from .models import Post, PostResponses, Email
from django.conf import settings


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_list.html'
    ordering = 'time'
    paginate_by = 5
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class MyPosts(ListView):
    model = Post
    template_name = 'my_posts.html'
    context_object_name = 'my_posts'

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user).order_by('time')
        return queryset


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['is_response'] = not PostResponses.objects.filter(post_id=self.kwargs['pk'],  # Проверка что такого
                                                                  user_id=self.request.user.id).exists()  # отклика еще нет
        context['responses'] = PostResponses.objects.filter(post_id=self.kwargs['pk'])  # Текущий отклик
        return context


class DetailResponse(LoginRequiredMixin, DetailView):
    model = PostResponses
    template_name = 'detail_response.html'
    context_object_name = 'detail_response'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accept = PostResponses.objects.get(id=self.kwargs['pk'])
        context['is_accept'] = accept.is_accept
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'post_create.html'
    success_url = '/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/'


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = PostResponses
    template_name = 'response_delete.html'
    success_url = '/'


class CreateResponse(LoginRequiredMixin, CreateView):
    model = PostResponses
    fields = ('text',)
    template_name = 'create_response.html'
    success_url = '/'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.user = self.request.user
        response.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


@login_required
def accept_response(_, pk):
    response = PostResponses.objects.get(id=pk)
    response.is_accept = True
    response.save()

    send_mail(
        subject=f'Пользователь {response.post.author} принял ваш отклик',
        message=response.text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.user.email, ]
    )

    return redirect(f'/response/detail/{response.id}')


class SendEmail(CreateView):
    model = Email
    template_name = 'send_email.html'
    fields = ('text',)
    success_url = '/'

    def form_valid(self, form):
        response = form.save(commit=False)
        users = User.objects.all()
        emails = []

        for i in users:
            emails.append(i.email)

        send_mail(
            subject='Рассылка новостей',
            message=response.text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails
        )
        return super().form_valid(form)
