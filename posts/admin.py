from django.contrib import admin
from posts.models import Category, PostItem
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(PostItem, MarkdownxModelAdmin)
admin.site.register(Category)

