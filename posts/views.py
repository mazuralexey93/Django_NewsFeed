from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from posts.models import PostItem, Category
from common.views import CommonContextMixin



class ItemsListView(ListView, CommonContextMixin):
    model = PostItem
    queryset = PostItem.objects.all()
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

