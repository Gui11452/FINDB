from django.urls import path
from . import views

urlpatterns = [
    path('planos/', views.planos, name='planos'),
    path('create_session/<str:tipo_pagamento>/<str:info>/', views.create_session, name='create_session'),
    path('webhook/', views.webhook, name='webhook'),
    path('upgrade_plan/<str:plano>/', views.upgrade_plan, name='upgrade_plan'),
    
    path('perfil_cancelamento_assinatura/', views.perfil_cancelamento_assinatura, name='perfil_cancelamento_assinatura'),
    path('excluir_perfil/<str:codigo>/', views.excluir_perfil, name='excluir_perfil'),
    path('perfil_excluido/', views.perfil_excluido, name='perfil_excluido'),

    # path('gerenciamento_assinatura/', views.gerenciamento_assinatura, name='gerenciamento_assinatura'),
    path('success/', views.success, name='success'),
    path('upgrade_success/', views.upgrade_success, name='upgrade_success'),
    path('reject/', views.reject, name='reject'),
    path('payment_event_success/', views.payment_event_success, name='payment_event_success'),

    path('atualizar_preco/', views.atualizar_preco, name='atualizar_preco'),
]