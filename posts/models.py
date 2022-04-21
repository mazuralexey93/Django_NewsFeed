from django.db import models
from authapp.models import User

class Category(models.Model):
    title = models.CharField(verbose_name='Название Категории', max_length=255)

    def __str__(self):
        return self.title

class PostItem(models.Model):

    title = models.CharField(verbose_name='Название', max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(verbose_name='Дата добавления', auto_created=True, auto_now_add=True)

    public = models.BooleanField(default=True)
    private = models.BooleanField(default=False)

    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    author = models.ForeignKey(User,on_delete=models.PROTECT)

    def __str__(self):
        return self.title
