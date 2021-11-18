from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'birthDay', 'SEX', 'registration_date', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active','SEX', 'registration_date']
    list_display_links = ['id','user']

admin.site.register(Profile, ProfileAdmin)
