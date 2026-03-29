"""
URL configuration for mathmatics project.

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
from src import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homefunc, name='home-page'),
    path('iujhtrewsgh765bh', views.pagehome, name='home-page-details'),
    path('h7oi09866tyr', views.loginPage, name='seconnecter'),
    path('hytrewsdf', views.blankpage, name='accueil'),
    path('uterfpolmterds', views.create_teacher, name='new-teacher'),
    path('58ju487kdfr124', views.sub_registration, name='sub-registration'),
    path('iuyte77kdfr8u', views.sub_list_categorie, name='sub-listcateg'),
    path('r124jhu78lpou78', views.StudyLevel, name='sutylevel'),
    path('huy79u78luy9869', views.Speciality, name='speciality'),
    path('pouy9869gtreza78', views.Commune, name='commune'),
    path('8khiuy9635z32y', views.Matiere, name='matiere'),
    path('uy962ythgyy654cxds', views.find_prof, name='search-prof'),
    path('uy650zEuVju6544fc/<int:id>/12', views.create_call , name='new-call'),
    path('hytgvggfvbg765f', views.list_commune, name='list-com'),
    path('fvhyt654dfebgd', views.list_studylevel, name='list-studylev'),
    path('ebjhuy654rfred', views.list_speciality, name='list-speciality'),

]
