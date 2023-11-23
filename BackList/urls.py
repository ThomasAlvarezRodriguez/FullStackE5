"""
URL configuration for CheckList project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from App_Checklist import views
from App_Checklist.views import jeux_list


urlpatterns = [
    path('', views.home_view, name='home'),
    path('profil/', views.profile_view, name='profile'),
    path('jeu/', views.game_view, name='game'),
    path('jeux/', jeux_list, name='jeux_list'),
    path('admin/', admin.site.urls),
]
