from django import forms
from markdownx.fields import MarkdownxFormField

from posts.models import User


class PostForm(forms.Form):
    myfield = MarkdownxFormField()
