# import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.urls import reverse


def photo_upload(instance, filename):
    """
    makes dir for uploading photo as
    media/article_images/[username]/[article_id]/photo
    and delete old photo if it is updating article
    """

    return f'article_images/{instance.author.username}/{filename}'


class Article(models.Model):
    views = IntegerField('Views', default=0)
    title = models.CharField(verbose_name="başlıq", max_length=50)
    author = models.ForeignKey(User, verbose_name="müəllif", on_delete=models.CASCADE, related_name="articles")
    category = models.ForeignKey('Category',verbose_name='Kateqoriya', on_delete=models.CASCADE, related_name='articles')
    content = models.TextField(verbose_name='məzmun', max_length=5000)
    created_at = models.DateTimeField('yaradılma tarixi', auto_now_add=True)
    updated_at = models.DateTimeField('sonuncu dəfə yenilənib', auto_now= True)
    drafted = models.BooleanField('qaralama', default=False)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField('şəkil', upload_to = photo_upload, blank=True)


    def get_absolute_url(self):
        return reverse('art_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title} - {self.author}'

    def save(self, *args, **kwargs):
        from PIL import Image
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
        img.save(self.photo.path)


class Category(models.Model):
    name = models.CharField(verbose_name='Kateqoriya:', max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=CASCADE, related_name='comments')
    author = models.ForeignKey(User, related_name='comments', on_delete=CASCADE)
    body = models.TextField('Comment', max_length=500)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)
    is_active = models.BooleanField('Active', default=True)

    class Meta:
        ordering = ('-created_at',)
    
    def ___str___(self):
        return f"Comment[{self.name}]:{self.article.title}"

# class Comment(models.Model):
#     article = models.ForeignKey(Article, on_delete=CASCADE, related_name='comments')
#     author = models.ForeignKey(User, related_name='comments', on_delete=CASCADE)
#     body = models.CharField('Comment', max_length=1000)
#     created_at = models.DateTimeField('Created at', auto_now_add=True)
#     updated_at = models.DateTimeField('Updated at', auto_now=True)
#     is_active = models.BooleanField('Active', default=True)

#     class Meta:
#         ordering = ('-created_at',)
    
#     def ___str___(self):
#         return f"Comment[{self.user.username}]:{self.article.title}"
    