from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('article.urls')),
    path('register/', user_views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'user/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name = 'logout'),
    # path('profile/', user_views.profile, name='profile'),
    path('update_profile/', user_views.profile_update, name='update_profile'),
    # path('update_profile/', user_views.ProfileUpdate.as_view(
    #                             template_name = 'user/update_profile.html'), name='update_profile'),
    path('profile/<str:username>', user_views.profile, name = 'profile'),
    path('profile/delete//<int:pk>', user_views.UserDelete.as_view(), name='user_delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
