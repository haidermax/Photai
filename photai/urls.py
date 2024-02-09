"""photai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from photos.views import *
from index.views import index, search
from accounts.views import PasswordResetView, PasswordResetConfirmView,login_page,register,activate, user_profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    path('login/', login_page, name='login'),
    
    path('logout', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

    # path("password_reset", password_reset_request, name="password_reset"),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('profile/', user_profile, name='profile'),
    path('result/<id>', listUploaderPhotos, name='userListPhoto'),

    path('', index, name='index'),
    path('photoDetails/<id>', photoDetails, name='details'),
    path('editPost/<id>', editPost, name='edit'),
    path('upload/', postCreate, name='upload'),
    path('like/', like_photo, name='like_photo'),
    path('category/<id>', category, name='category'),
    # Search
    path('searching/', search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
