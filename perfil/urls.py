from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),

    path('registrar_conta/<str:codigo>/', views.registrar_conta, name='registrar_conta'),

    path('logout/', views.logout, name='logout'),
    path('info/<str:slug>/', views.perfil, name='perfil'),
    path('filtro/pessoas/', views.filtro, name='filtro'),
    path('meu_perfil/', views.meu_perfil, name='meu_perfil'),

    path('alterar_dados/', views.alterar_dados, name='alterar_dados'),

    path('convidar/', views.convidar, name='convidar'),
    path('convite_enviado/', views.convite_enviado, name='convite_enviado'),

    path('reconfirmacao_email/<str:codigo>/<str:email>/', views.reconfirmar_email, name='reconfirmar_email'),
    path('confirmacao_email/<str:codigo>/', views.confirmar_email, name='confirmar_email'),
    path('esqueceu_senha/', views.esqueceu_senha, name='esqueceu_senha'),
    path('recuperacao_senha/<str:codigo>/', views.recuperacao_senha, name='recuperacao_senha'),

    path('cupido/<str:slug>/', views.cupido, name='cupido'),

    path('meus_eventos/', views.meus_eventos, name='meus_eventos'),
    
    path('chamadas_video/', views.chamadas_video, name='chamadas_video'),
    path('chamada_video/<int:id>/', views.chamada_video, name='chamada_video'),
    path('confirmar_chamada_video/<int:id>/', views.confirmar_chamada_video, name='confirmar_chamada_video'),

    path('convite_chamada_video_enviado/<int:id>/', views.convite_chamada_video_enviado, name='convite_chamada_video_enviado'),
    path('convite_chamada_video/', views.convite_chamada_video, name='convite_chamada_video'),

    # path('teste/', views.teste, name='teste'),
    # path('teste_sucesso/', views.teste_sucesso, name='teste_sucesso'),

    path('criar_perfis_fakes/', views.criar_perfis_fakes, name='criar_perfis_fakes'),
]