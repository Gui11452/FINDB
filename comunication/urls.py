from django.urls import path
from . import views

urlpatterns = [
    path('send_notification_comunication/', views.send_notification_comunication, name='send_notification_comunication'),
    path('comunication_call/<str:roomID>/', views.comunication_call, name='comunication_call'),

    path('get_comunications/<str:slug_perfil>/', views.get_comunications, name='get_comunications'),
    path('get_comunication/<int:id>/', views.get_comunication, name='get_comunication'),

    path('confirmar_chamada/<int:id>/', views.confirmar_chamada, name='confirmar_chamada'),
    path('rejeitar_chamada/<int:id>/', views.rejeitar_chamada, name='rejeitar_chamada'),

    path('bloquear_usuario/<str:slug_destinatario>/', views.bloquear_usuario, name='bloquear_usuario'),
    path('desbloquear_usuario/<str:slug_destinatario>/', views.desbloquear_usuario, name='desbloquear_usuario'),
]