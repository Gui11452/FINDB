from django.contrib import admin
from .models import Perfil, Cupido, RecuperacaoSenha, Album, VideoChamada, ColaboradoresEvento
from django.contrib.auth.models import User

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_email', 'genero', 'pais', 'interesse', 'orientacao_sexual', 'estado_civil', 'profissao', 'etnia', 'idade', 'aniversario', 'verificacao_email')
    list_display_links = ('nome', 'get_email', 'genero', 'pais', 'interesse', 'orientacao_sexual', 'estado_civil', 'profissao', 'etnia', 'idade', 'aniversario', 'verificacao_email')
    list_filter = ('genero', 'pais', 'interesse', 'orientacao_sexual', 'estado_civil', 'etnia', 'idade', 'aniversario', 'verificacao_email')
    list_per_page = 20
    readonly_fields = ('get_email', 'slug', 'codigo', 'codigo_cancelar_assinatura', 'last_activity')
    search_fields = ('usuario__username', 'nome', 'genero', 'pais', 'interesse', 'orientacao_sexual', 'estado_civil', 'profissao', 'etnia')

admin.site.register(Perfil, PerfilAdmin)

class CupidoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'foto', 'pais', 'cidade', 'link')
    list_display_links = ('nome', 'email', 'foto', 'pais', 'cidade', 'link')
    list_filter = ('pais',)
    list_per_page = 20
    readonly_fields = ('slug', 'link', 'codigo', 'usuario')
    search_fields = ('nome', 'email')

admin.site.register(Cupido, CupidoAdmin)

class ColaboradoresEventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_email', 'regiao', 'pais', 'celular')
    list_display_links = ('nome', 'get_email', 'regiao', 'pais', 'celular')
    list_filter = ('pais',)
    list_per_page = 20
    readonly_fields = ('slug', 'codigo', 'usuario')
    search_fields = ('nome', 'get_email')

admin.site.register(ColaboradoresEvento, ColaboradoresEventoAdmin)


class RecuperacaoSenhaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'codigo', 'data' ,'recuperacao')
    list_display_links = ('usuario', 'codigo', 'data' ,'recuperacao')
    list_filter = ('recuperacao', 'data')
    list_per_page = 10
    search_fields = ('usuario__username',)
    readonly_fields = ('codigo',)

admin.site.register(RecuperacaoSenha, RecuperacaoSenhaAdmin)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'foto1', 'foto2', 'foto3', 'foto4', 'foto5')
    list_display_links = ('perfil', 'foto1', 'foto2', 'foto3', 'foto4', 'foto5')
    list_per_page = 10

admin.site.register(Album, AlbumAdmin)

class VideoChamadaAdmin(admin.ModelAdmin):
    list_display = ('data', 'remetente', 'destinatario', 'confirmacao')
    list_display_links = ('data', 'remetente', 'destinatario', 'confirmacao')
    list_filter = ('data', 'confirmacao')
    list_per_page = 10

admin.site.register(VideoChamada, VideoChamadaAdmin)