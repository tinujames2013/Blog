# Generated by Django 5.0.6 on 2024-11-25 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0004_alter_blog_blog_image_alter_blog_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
