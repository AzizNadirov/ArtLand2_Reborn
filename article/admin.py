from django.contrib import admin
from .models import Article, Category, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'updated_at', 'photo', 'drafted', 'views']
    list_editable = ['author', 'category', 'drafted']
    list_filter = ['drafted', 'drafted', 'category', 'views']
    list_display_links = ['id','title']
    exclude = ['views']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'created_at', 'is_active']
    list_filter = ['is_active', 'article', 'created_at']
    list_editable = ['is_active']
    list_display_links = ['author', 'article']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)