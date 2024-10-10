from django.contrib import admin
from .models import Evento, Notificacao, ParticipantesEvento, ConviteEvento, GaleriaEvento, Item, AtividadeTuristica, Lugar, DetalheDia, PerguntaFrequente, Categoria

class GaleriaEventoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'foto1', 'foto2', 'foto3', 'foto4', 'foto5')
	list_display_links = ('nome', 'foto1', 'foto2', 'foto3', 'foto4', 'foto5')
	list_per_page = 20
	search_fields = ('nome',)
admin.site.register(GaleriaEvento, GaleriaEventoAdmin)

class ItemAdmin(admin.ModelAdmin):
	list_display = ('texto',)
	list_display_links = ('texto',)
	list_per_page = 20
	search_fields = ('texto',)
admin.site.register(Item, ItemAdmin)

class AtividadeTuristicaAdmin(admin.ModelAdmin):
	list_display = ('texto',)
	list_display_links = ('texto',)
	list_per_page = 20
	search_fields = ('texto',)
admin.site.register(AtividadeTuristica, AtividadeTuristicaAdmin)

class LugarAdmin(admin.ModelAdmin):
	list_display = ('texto',)
	list_display_links = ('texto',)
	list_per_page = 20
	search_fields = ('texto',)
admin.site.register(Lugar, LugarAdmin)

class DetalheDiaAdmin(admin.ModelAdmin):
	list_display = ('texto',)
	list_display_links = ('texto',)
	list_per_page = 20
	search_fields = ('texto',)
admin.site.register(DetalheDia, DetalheDiaAdmin)

class PerguntaFrequenteAdmin(admin.ModelAdmin):
	list_display = ('nome', 'texto')
	list_display_links = ('nome', 'texto')
	list_per_page = 20
	search_fields = ('nome', 'texto')
admin.site.register(PerguntaFrequente, PerguntaFrequenteAdmin)

class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	list_display_links = ('nome',)
	list_per_page = 10
	search_fields = ('nome',)

admin.site.register(Categoria, CategoriaAdmin)

class EventoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'tipo', 'data', 'data_termino', 'pagamento', 'valor', 'visibilidade', 'divisao_genero', 'get_qtd_vagas')
	list_display_links = ('nome', 'tipo', 'data', 'data_termino', 'pagamento', 'valor', 'divisao_genero', 'get_qtd_vagas')
	list_per_page = 10
	list_editable = ('visibilidade',)
	list_filter = ('tipo', 'data', 'pagamento', 'visibilidade', 'divisao_genero')
	readonly_fields = ('slug', 'codigo', 'qtd_participantes', 'qtd_participantes_homens', 'qtd_participantes_mulheres')
	search_fields = ('nome',)

admin.site.register(Evento, EventoAdmin)

class ParticipantesEventoAdmin(admin.ModelAdmin):
	list_display = ('evento', 'remetente', 'confirmacao', 'comparecer_evento')
	list_display_links = ('evento', 'remetente', 'confirmacao', 'comparecer_evento')
	list_filter = ('comparecer_evento',)
	list_per_page = 10
	list_filter = ('evento',)

admin.site.register(ParticipantesEvento, ParticipantesEventoAdmin)

class NotificacaoAdmin(admin.ModelAdmin):
	list_display = ('tipo', 'convite_evento', 'video_chamada', 'confirmacao')
	list_display_links = ('tipo', 'convite_evento', 'video_chamada', 'confirmacao')
	list_per_page = 10
	list_filter = ('tipo', 'confirmacao')

admin.site.register(Notificacao, NotificacaoAdmin)

class ConviteEventoAdmin(admin.ModelAdmin):
	list_display = ('evento', 'remetente', 'destinatario', 'confirmacao')
	list_display_links = ('evento', 'remetente', 'destinatario', 'confirmacao')
	list_per_page = 10
	list_filter = ('confirmacao', 'evento')

admin.site.register(ConviteEvento, ConviteEventoAdmin)
