from django.db import models

class Category(models.Model):
    title = models.CharField(verbose_name='Название Категории', max_length=255)

    def __str__(self):
        return self.title

class PostItem(models.Model):

    title = models.CharField(verbose_name='Название', max_length=255)
    author = models.CharField(verbose_name='Автор', max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(verbose_name='Дата добавления', auto_created=True, auto_now_add=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.title
