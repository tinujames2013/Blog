# Generated by Django 5.0.6 on 2024-10-22 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitevisitor', '0002_alter_blog_author_alter_blog_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blog',
        ),
    ]
