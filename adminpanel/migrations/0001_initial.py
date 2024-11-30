# Generated by Django 5.0.6 on 2024-09-17 08:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_description', models.TextField()),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('profile_image', models.ImageField(upload_to='profile_images/')),
                ('id_proof', models.ImageField(upload_to='id_proofs/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]