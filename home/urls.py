from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home_filtro/', views.home_filtro, name='home_filtro'),
    path('cupidos/', views.cupidos, name='cupidos'),
    path('profissionais_relacionamento/', views.profissionais_relacionamento, name='profissionais_relacionamento'),
    path('profissional/<str:uid>/', views.profissional, name='profissional'),
]