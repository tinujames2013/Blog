# Generated by Django 5.0.6 on 2024-11-25 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0005_alter_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
