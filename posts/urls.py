from django.urls import path
from posts.views import ItemsListView

app_name = 'posts'

urlpatterns = [
    path('', ItemsListView.as_view(), name='index'),

]