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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('profil/', views.profile_view, name='profile'),
    path('jeu/', views.game_view, name='game'),
    path('jeux/<int:jeu_id>/', views.game_detail, name='game_detail'),
    path('jeux/', jeux_list, name='jeux_list'),
    path('admin/', admin.site.urls),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('quetes/<int:quete_id>/', views.quete_detail, name='quete_detail'),
    path('profil/', views.profile_view, name='profile'),
    path('connexion/', auth_views.LoginView.as_view(template_name='connexion.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('favoris/<int:jeu_id>/', views.toggle_favoris, name='toggle_favoris'),
    path('toggle-obtenu-item/<int:item_id>/', views.toggle_obtenu_item, name='toggle_obtenu_item'),
    path('toggle-obtenu-quete/<int:quete_id>/', views.toggle_obtenu_quete, name='toggle_obtenu_quete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)