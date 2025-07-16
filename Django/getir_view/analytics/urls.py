from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('orders/', views.siparis_list, name='siparis_list'),
    path('sip-per-capita/', views.sip_per_capita, name='sip_per_capita'),
    path('sip-density-per-hood/', views.sip_density_per_hood, name='sip_density_per_hood'),

    
]
