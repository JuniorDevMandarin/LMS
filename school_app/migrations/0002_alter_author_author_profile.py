# Generated by Django 4.2.1 on 2024-06-11 13:47

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_profile',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]