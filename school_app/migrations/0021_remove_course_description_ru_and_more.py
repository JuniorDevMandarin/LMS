# Generated by Django 4.2.1 on 2024-06-10 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0020_alter_course_featured_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='description_ru',
        ),
        migrations.RemoveField(
            model_name='course',
            name='featured_video',
        ),
        migrations.RemoveField(
            model_name='course',
            name='stripe_price_id',
        ),
        migrations.RemoveField(
            model_name='course',
            name='title_ru',
        ),
    ]
