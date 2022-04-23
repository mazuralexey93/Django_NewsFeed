from django import forms
from markdownx.fields import MarkdownxFormField

from posts.models import PostItem


class PostForm(forms.ModelForm):

    class Meta:
        model = PostItem
        fields = ('title', 'text', 'private', 'category', 'delete_flag')

    text = MarkdownxFormField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

class DeleteForm(forms.ModelForm):
    class Meta:
        model = PostItem
        fields = ('delete_flag', )
