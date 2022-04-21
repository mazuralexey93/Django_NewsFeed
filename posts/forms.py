from django import forms
from markdownx.fields import MarkdownxFormField

from maincatapp.models import UserPost


class PostForm(forms.Form):
    myfield = MarkdownxFormField()
