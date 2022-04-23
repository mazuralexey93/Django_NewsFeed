from django.urls import path, include
from posts.views import PostsListView, PrivatePostsListView, PostReaderView, UserPostView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

app_name = 'posts'

urlpatterns = [
    path('', PostsListView.as_view(), name='postslist'),
    path('filtered/', login_required(PrivatePostsListView.as_view()), name='secretpostslist'),
    path('post/<post_id>', PostReaderView.as_view(), name='post'),
    path('all/', UserPostView.as_view(), name='usersposts'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)