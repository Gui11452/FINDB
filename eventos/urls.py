from django.urls import path
from . import views

urlpatterns = [
    path('presenciais/', views.presenciais, name='presenciais'),
    path('online/', views.online, name='online'),
    path('info/<str:slug>/', views.evento, name='evento'),

    path('convidar/<str:slug_destinatario>/', views.convidar_evento, name='convidar_evento'),

    path('rejeitar_notificacao/<int:id>/', views.rejeitar_notificacao, name='rejeitar_notificacao'),

    path('aprovar_entrada_evento/<str:codigo>/', views.aprovar_entrada_evento, name='aprovar_entrada_evento'),
    path('cadastrar_colaboradores_evento/', views.cadastrar_colaboradores_evento, name='cadastrar_colaboradores_evento'),

    path('galeria_fotos/<str:slug>/', views.galeria_fotos, name='galeria_fotos'),

    path('notificacoes/<str:slug>/', views.notificacoes, name='notificacoes'),
    path('apagar_notificacao/<int:id>/', views.apagar_notificacao, name='apagar_notificacao'),
]