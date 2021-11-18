from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

from ArtLand2_Reborn.settings import MEDIA_ROOT


def photo_upload(instance, filename):
    dir = os.path.join(MEDIA_ROOT,'profile_images',f'{instance.user.username}' )
    walk = list(os.walk(dir))
    try:
        for old_photo in walk[-1][-1]:
            os.remove(os.path.join(dir,old_photo))
    except: IndexError
    return f'profile_images/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField('Biography', max_length=250, blank=True, null = True)
    photo = models.ImageField('Photo',upload_to = photo_upload, default = "profile_images/default_avatar.jpg", blank=True)
    birthDay = models.DateField('Birth Day', null = True)
    SEX_CHOICES = [('Male', 'Male'),
        ('Female', 'Female'),
        ('Empty', 'Do not Show')]
    SEX = models.CharField('Sex', choices=SEX_CHOICES, max_length=10, default='x')
    is_active = models.BooleanField("Active", default=True)
    registration_date = models.DateField('User registration date',auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.photo:
            self.photo = f"{os.path.join(MEDIA_ROOT, 'profile_images')}/default_avatar.jpg"
        else:
            img = Image.open(self.photo.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.path)
