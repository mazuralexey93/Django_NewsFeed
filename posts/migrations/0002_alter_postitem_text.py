# Generated by Django 4.0.4 on 2022-04-21 19:59

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postitem',
            name='text',
            field=markdownx.models.MarkdownxField(),
        ),
    ]