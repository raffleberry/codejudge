# Generated by Django 2.2 on 2020-04-14 18:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_auto_20200414_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='users',
        ),
        migrations.AddField(
            model_name='session',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
