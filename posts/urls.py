from django.urls import path, include
from posts.views import ItemsListView, ItemsPrivateListView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    path('', ItemsListView.as_view(), name='postslist'),
    path('filtered/', ItemsPrivateListView.as_view(), name='secretpostslist'),
    # path('post/<int:pk>/', product, name='post'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)