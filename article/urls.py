from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('articles/', ArtList.as_view(), name='article_list'),
    path('<int:pk>/', ArtDetail.as_view(), name='art_detail'),
    path('new/', ArtCreate .as_view(), name='art_create'),
    path('<int:pk>/update/', ArtUpdate.as_view(), name='art_update'),
    path('<int:pk>/delete/', ArtDelete.as_view(), name='art_delete'),
]
