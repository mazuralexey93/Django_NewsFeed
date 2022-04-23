from django.contrib import admin
from posts.models import Category, PostItem


admin.site.register(PostItem)
admin.site.register(Category)
