from django.urls import path, include
from posts.views import ItemsListView

app_name = 'posts'

urlpatterns = [
    path('', ItemsListView.as_view(), name='postslist'),

]