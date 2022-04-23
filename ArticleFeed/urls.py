"""ArticleFeed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from . import views
from django.contrib.auth.decorators import login_required


from posts import urls as posts_urls
from authapp import urls as authapp_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),


    path('posts/', include(posts_urls, namespace='posts'), name='posts'),
    path('auth/', include(authapp_urls, namespace='auth'), name='auth'),
]
