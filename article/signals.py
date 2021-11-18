# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Article
# from ArtLand2_Reborn.settings import MEDIA_ROOT
# import os



# # instance created object

# @receiver(post_save, sender = Article)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         dir = os.path.join(MEDIA_ROOT,'article_images',f'{instance.author.username}', f'' )
#         # walk = list(os.walk(dir))
#         # try:
#         #     for old_photo in walk[-1][-1]:
#         #         os.remove(os.path.join(dir,old_photo))
#         # except: IndexError

#         # prof = Profile.objects.create(user = instance)
#         # prof.save()