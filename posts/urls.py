from django.urls import path, include
from posts.views import PostsListView, PrivatePostsListView, PostReaderView, UserPostView, post_new, post_edit, post_delete, DeleteView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


app_name = 'posts'

urlpatterns = [
    path('', PostsListView.as_view(), name='postslist'),
    path('filtered/', login_required(PrivatePostsListView.as_view()), name='secretpostslist'),
    path('post/<int:pk>/', PostReaderView.as_view(), name='detailpost'),
    path('my/', UserPostView.as_view(), name='usersposts'),
    path('new/', post_new, name='newpost'),
    path('post/<int:pk>/edit/', post_edit, name='editpost'),
    path('post/<int:pk>/delete/', post_delete, name='deletepost'),
    # path('post/<int:pk>/delete/', DeleteView.as_view(), name='deletepost'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
