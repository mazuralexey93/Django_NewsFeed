from django.shortcuts import render
from django.views.generic.list import ListView
from posts.models import PostItem, Category
from posts.forms import PostForm


class ItemsListView(ListView):
    model = PostItem
    queryset = PostItem.objects.filter(public=True).order_by('-created_at')
    template_name = "postlist.html"
    title = 'Posts'

    def get_queryset(self):
        queryset = super(ItemsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ItemsListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ItemsPrivateListView(ItemsListView):
    queryset = PostItem.objects.filter(private=True).order_by('-created_at')
    template_name = "secret_postlist.html"
    title = 'Secret Posts'


class PostReaderView(ListView):
    form_class = PostForm
    template_name = 'post.html'

    def get(self, request, post_id):
        categories = Category.objects.all().order_by('-title')
        post = PostItem.objects.get(id=post_id)
        context = {
            'title': post.title,
            'categories': categories,
            'post': post
        }
        return render(request, self.template_name, context)
