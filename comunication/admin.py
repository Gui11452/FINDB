from django.contrib import admin
from .models import Comunication, BloquearUsuarios

class ComunicationAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'destinatario', 'tipo', 'confirmacao', 'data')
    list_display_links = ('remetente', 'destinatario', 'tipo', 'confirmacao', 'data')
    list_filter = ('tipo', 'confirmacao', 'data')
    list_per_page = 20
    search_fields = ('remetente__nome', 'destinatario__nome')

admin.site.register(Comunication, ComunicationAdmin)

class BloquearUsuariosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'bloqueado')
    list_display_links = ('usuario', 'bloqueado')
    list_per_page = 20
    search_fields = ('usuario__nome', 'bloqueado__nome')

admin.site.register(BloquearUsuarios, BloquearUsuariosAdmin)
