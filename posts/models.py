from django.db import models
from authapp.models import User

from django.utils.safestring import mark_safe
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from bleach import clean


class Category(models.Model):
    title = models.CharField(verbose_name='Название Категории', max_length=255)

    def __str__(self):
        return self.title


class PostItem(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    text = MarkdownxField()
    created_at = models.DateTimeField(verbose_name='Дата добавления', auto_created=True, auto_now_add=True)

    public = models.BooleanField(default=True)
    private = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    @property
    def formatted_markdown(self):
        body = self.text

        dirty_data = mark_safe(markdownify(body))
        clean_data = clean(
            dirty_data,
            tags=[
                'a', 'abbr', 'acronym', 'b', 'blockquote', 'blockquotes', 'code', 'em', 'i', 'li',
                'ol', 'strong', 'ul', 'img', 'p', 'quote'],
            attributes={
                'a': ['href', 'target', 'title'],
                'img': ['src', 'alt', 'width', 'height'],

            },
            strip=True
        )
        return clean_data
