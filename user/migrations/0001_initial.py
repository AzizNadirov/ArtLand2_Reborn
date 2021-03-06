# Generated by Django 3.2.7 on 2021-09-22 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user.models


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
                ('bio', models.TextField(blank=True, max_length=250, null=True, verbose_name='Biography')),
                ('photo', models.ImageField(blank=True, default='profile_images/default_avatar.jpg', upload_to=user.models.photo_upload, verbose_name='Photo')),
                ('birthDay', models.DateField(null=True, verbose_name='Birth Day')),
                ('SEX', models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('x', 'Do not Show')], default='x', max_length=10, verbose_name='Sex')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('registration_date', models.DateField(auto_now_add=True, null=True, verbose_name='User registration date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
