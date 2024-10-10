from django.db import models
from perfil.models import Perfil
from eventos.models import Evento

class Plano(models.Model):
    nome = models.CharField(
        default='tres_meses',
        max_length=255, 
        verbose_name="Nome", 
        choices=[
            ("tres_meses", "Três Meses"),
            ("seis_meses", "Seis Meses"),
            ("doze_meses", "Doze Meses"),

            ("tres_meses_promocional", "Três Meses Promocional"),
            ("seis_meses_promocional", "Seis Meses Promocional"),
            ("doze_meses_promocional", "Doze Meses Promocional"),
        ],
    )
    preco = models.FloatField(default=0, verbose_name='Preco')
    codigo = models.CharField(max_length=2000, default='', verbose_name='Código', unique=True)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return f'{self.nome}'


class Pedido(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.SET_NULL, verbose_name="Perfil", blank=True, null=True)

    preco_pedido = models.FloatField(default=0, verbose_name="Preço do pedido")
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Data do pedido")
    data_ultima_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data da Última Atualização", blank=True, null=True)

    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, verbose_name="Plano", blank=True, null=True)

    status_pedido = models.CharField(
		default='pending',
		max_length=20,
		choices=(
			('approved', 'approved'),
            ('cancel', 'cancel'),
            ('paused', 'paused'),
			('rejected', 'rejected'),
            ('pending', 'pending'),
		), 
		verbose_name="Status Pedido",
	)

    evento_gratis = models.CharField(
		default='nao',
		max_length=20,
		choices=(
			('nao', 'nao'),
            ('sim', 'sim'),
		), 
		verbose_name="Tem direito a 1 evento grátis?",
	)
    qtd_eventos_gratis = models.IntegerField(default=0, verbose_name="Quantidade de Eventos Grátis")

    id_user = models.CharField(default='', max_length=1000, verbose_name="Id User")
    id_assinatura = models.CharField(default='', max_length=1000, verbose_name="Id Assinatura")
    current_period_end = models.IntegerField(default=0, verbose_name="Current Period End")
    
    plano_ativo = models.BooleanField(default=False, verbose_name="Plano Ativo")

    recebeu_email_aprovado = models.BooleanField(default=False, verbose_name="Código Interno AP")
    recebeu_email_reprovado = models.BooleanField(default=False, verbose_name="Código Interno REP")
    recebeu_email_pendente = models.BooleanField(default=False, verbose_name="Código Interno PEN")

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        if self.perfil:
            return f'{self.perfil.nome}'
        return f'{self.id}'
        


class PagamentoEventos(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.SET_NULL, verbose_name="Perfil", blank=True, null=True)

    preco_pedido = models.FloatField(default=0, verbose_name="Preço do pedido")
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Data do pedido")

    qtd_criancas = models.IntegerField(default=0, verbose_name="Quantidade de Crianças")
    
    status_pedido = models.CharField(
		default='pending',
		max_length=20,
		choices=(
			('approved', 'approved'),
			('rejected', 'rejected'),
            ('pending', 'pending'),
            ('refund', 'refund'),
		), 
		verbose_name="Status Pedido",
	)
    
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL, verbose_name='Evento', blank=True, null=True)

    payment_intent = models.CharField(default='', max_length=2000 ,verbose_name="Payment Intent")
    id_reembolso = models.CharField(default='', max_length=2000 ,verbose_name="Reembolso ID", blank=True, null=True)

    pagamento_feito = models.BooleanField(default=False, verbose_name="Pagamento Feito")

    recebeu_email_aprovado = models.BooleanField(default=False, verbose_name="Código Interno AP")
    recebeu_email_refund = models.BooleanField(default=False, verbose_name="Código Interno REF")
    recebeu_email_reprovado = models.BooleanField(default=False, verbose_name="Código Interno REP")
    recebeu_email_pendente = models.BooleanField(default=False, verbose_name="Código Interno PEN")

    class Meta:
        verbose_name = 'Pagamento Evento'
        verbose_name_plural = 'Pagamento Eventos'

    def __str__(self):
        if self.perfil:
            return f'{self.perfil.nome}'
        return f'{self.id}'
