from django.contrib import admin
from .models import Plano, Pedido, PagamentoEventos

class PlanoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'preco')
	list_display_links = ('nome', 'preco')
	list_filter = ('nome', 'preco')
	search_fields = ('nome',)
	list_per_page = 20

admin.site.register(Plano, PlanoAdmin)

class PedidoAdmin(admin.ModelAdmin):
	list_display = ('perfil', 'preco_pedido', 'data_pedido', 'data_ultima_atualizacao', 'plano', 'status_pedido', 'plano_ativo', 'evento_gratis')
	list_display_links = ('perfil', 'preco_pedido', 'data_pedido', 'data_ultima_atualizacao', 'plano', 'status_pedido', 'plano_ativo', 'evento_gratis')
	list_filter = ('plano', 'status_pedido', 'plano_ativo', 'evento_gratis')
	search_fields = ('perfil__nome',)
	list_per_page = 20

admin.site.register(Pedido, PedidoAdmin)

class PagamentoEventosAdmin(admin.ModelAdmin):
	list_display = ('perfil', 'preco_pedido', 'data_pedido', 'status_pedido', 'pagamento_feito', 'evento', 'qtd_criancas')
	list_display_links = ('perfil', 'preco_pedido', 'data_pedido', 'status_pedido', 'pagamento_feito', 'evento', 'qtd_criancas')
	list_filter = ('pagamento_feito', 'evento')
	search_fields = ('perfil__nome',)
	list_per_page = 20

admin.site.register(PagamentoEventos, PagamentoEventosAdmin)
