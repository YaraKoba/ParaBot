"""service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from my_telebot.views import SpotsView, UserView, CityView

router = DefaultRouter()
router.register(r'users', UserView, basename='user')
router.register(r'city', CityView, basename='city')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/spots/', SpotsView.as_view(), name='spots_list'),
    path('api/', include(router.urls)),
    # path(r'api/auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
]

# urlpatterns += router.urls
