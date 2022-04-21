from django.shortcuts import render
from django.views.generic.list import ListView
from posts.models import PostItem, Category


class ItemsListView(ListView):
    model = PostItem
    queryset = PostItem.objects.filter(public=True)
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
    queryset = PostItem.objects.filter(private=True)
    template_name = "secret_postlist.html"
    title = 'Secret Posts'

# class PostListView(ListView):
#     def product(request, pk):
#         title = 'страница продута'
#
#
#         context = {
#             'title': title,
#             'categories': ProductCategory.objects.all(),
#             'product': get_object_or_404(Product, pk=pk),
#             'basket': get_basket(request.user),
#             'hot_product': hot_product,
#             'same_products': same_products,
#         }
#
#         return render(request, 'mainapp/product.html', context)
