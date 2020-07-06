"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

import store
from store import views
import users
from users import views as UsersViews

urlpatterns = [
    path('admin/', admin.site.urls),
    #import include function and add a path that points to the store's url.py 
    path('', include('store.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),


    
    path('register/', UsersViews.registerPage, name="register"),
	path('login/', UsersViews.loginPage, name="login"),  
    path('logout/', UsersViews.logoutUser, name="logout"),

]
# Accessing images using paths from the url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)