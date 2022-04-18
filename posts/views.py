from django.shortcuts import render
from django.views.generic.list import ListView
from posts.models import PostItem

class ItemsListView(ListView):
    model = PostItem
    template_name = "postlist.html"
    # queryset = PostItem.objects.all()

    def get_queryset(self):
        # queryset = PostItem.on_site.select_related('category').prefetch_related('new_category').all()
        # category_id = self.kwargs.get('category_id')
        # return queryset.filter(category_id=category_id) if category_id else queryset
        return PostItem.objects.all()


