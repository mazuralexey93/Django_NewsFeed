from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.views import View
from posts.models import PostItem, Category
from authapp.models import User
from posts.forms import PostForm, DeleteForm
from urllib import request
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.timezone import now

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator

class TestMixin1(UserPassesTestMixin):
    login_url = '/auth/edit/'

    def test_func(self, request):
        return request.user.role == 'sub'



class PostsListView(ListView):
    model = PostItem
    queryset = PostItem.objects.filter(public=True).order_by('-created_at')
    template_name = "postlist.html"
    title = 'Posts'

    def get_queryset(self):
        queryset = super(PostsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['posts'] = PostItem.objects.exclude(delete_flag=True).exclude(private=True).order_by('-created_at')
        return context

@user_passes_test(lambda user: user.role=='sub', login_url='/auth/edit/')
def private_posts(request):
    title = 'для подписчиков'
    categories = Category.objects.all()
    posts = PostItem.objects.exclude(delete_flag=True).filter(private=True).order_by('-created_at')

    context = {
        'title': title,
        'categories': categories,
        'posts': posts,
    }

    return render(request, 'secret_postlist.html', context=context)

class PrivatePostsListView(ListView, TestMixin1):
    model = PostItem
    queryset = PostItem.objects.filter(private=True).order_by('-created_at')
    template_name = "secret_postlist.html"
    title = 'Secret Posts'

    def get_queryset(self):
        queryset = super(PrivatePostsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(PrivatePostsListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['posts'] = PostItem.objects.exclude(delete_flag=True).filter(private=True).order_by('-created_at')
        return context


class PostReaderView(DetailView):
    form_class = PostForm
    template_name = 'post.html'
    context_object_name = 'post'

    def get(self, request, pk):
        categories = Category.objects.all().order_by('-title')
        post = PostItem.objects.get(pk=pk)
        context = {
            'title': post.title,
            'categories': categories,
            'post': post
        }
        return render(request, self.template_name, context)


class UserPostView(ListView):
    form_class = PostForm
    template_name = 'postlist.html'

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        # posts = PostItem.objects.exclude(delete_flag=True).filter(author_id=user).order_by('-created_at')
        posts = PostItem.objects.filter(author_id=user).order_by('-created_at')
        context = {
            'user': user,
            'posts': posts
        }
        return render(request, self.template_name, context)


@user_passes_test(lambda user: user.role=='auth', login_url='/auth/edit/')
def post_new(request):
    title = 'новая статья'
    if request.method == 'POST' :
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_at = now()
            post.save()
            return redirect('posts:detailpost', pk=post.pk)
    else:
        form = PostForm()

    context = {'form': form, 'title': title}
    return render(request, 'post_create.html', context)


def post_edit(request, pk):
    title = 'редактировать статью'
    post = get_object_or_404(PostItem, pk=pk)

    if request.method == 'GET':
        if request.user != post.author:
            return redirect('posts:detailpost', pk=post.pk)
        form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_at = now()
            post.save()
            return redirect('posts:detailpost', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {'form': form, 'title': title, 'post': post}
    return render(request, 'post_edit.html', context)


def post_delete(request, pk):
    title = 'удалить статью'
    post = get_object_or_404(PostItem, pk=pk)

    if request.method == 'GET':
        if request.user != post.author:
            return redirect('posts:detailpost', pk=post.pk)
        form = PostForm(instance=post)

    if request.method == "POST":
        form = DeleteForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.delete_flag = True
            post.save()
            return redirect('posts:usersposts')
    else:
        form = DeleteForm(instance=post)

    context = {'form': form, 'title': title, 'post': post}
    return render(request, 'post_delete.html', context)
