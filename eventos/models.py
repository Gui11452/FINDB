from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify
from perfil.models import Perfil, VideoChamada
import string
import random

# Configurações Evento - Início
class GaleriaEvento(models.Model):
    nome = models.CharField(max_length=1000, default='', verbose_name='Nome')
    foto1 = models.ImageField(blank=True, null=True, upload_to='galeria_eventos/%Y/%m/%d', verbose_name="Foto 1")
    foto2 = models.ImageField(blank=True, null=True, upload_to='galeria_eventos/%Y/%m/%d', verbose_name="Foto 2")
    foto3 = models.ImageField(blank=True, null=True, upload_to='galeria_eventos/%Y/%m/%d', verbose_name="Foto 3")
    foto4 = models.ImageField(blank=True, null=True, upload_to='galeria_eventos/%Y/%m/%d', verbose_name="Foto 4")
    foto5 = models.ImageField(blank=True, null=True, upload_to='galeria_eventos/%Y/%m/%d', verbose_name="Foto 5")

    class Meta:
        verbose_name = 'Galeria do Evento'
        verbose_name_plural = 'Galerias do Evento'

    def __str__(self):
        return f'{self.nome}'
    

class Item(models.Model):
    texto = models.TextField(max_length=3000, default='', verbose_name='Texto')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

    def __str__(self):
        return f'{self.texto}'
    
class AtividadeTuristica(models.Model):
    texto = models.TextField(max_length=3000, default='', verbose_name='Texto')

    class Meta:
        verbose_name = 'Atividade Turistica'
        verbose_name_plural = 'Atividades Turisticas'

    def __str__(self):
        return f'{self.texto}'
    
class Lugar(models.Model):
    texto = models.TextField(max_length=3000, default='', verbose_name='Texto')

    class Meta:
        verbose_name = 'Lugar'
        verbose_name_plural = 'Lugares'

    def __str__(self):
        return f'{self.texto}'
    
class DetalheDia(models.Model):
    texto = models.TextField(max_length=5000, default='', verbose_name='Texto')

    class Meta:
        verbose_name = 'Detalhe do Dia'
        verbose_name_plural = 'Detalhes dos Dias'

    def __str__(self):
        return f'{self.texto}'
    
class PerguntaFrequente(models.Model):
    nome = models.CharField(max_length=2000, default='', verbose_name='Pergunta')
    texto = models.TextField(max_length=5000, default='', verbose_name='Resposta')

    class Meta:
        verbose_name = 'Pergunta Frequente'
        verbose_name_plural = 'Perguntas Frequentes'

    def __str__(self):
        return f'{self.nome}'
    
class Categoria(models.Model):
    nome = models.CharField(max_length=2000, default='', verbose_name='Nome')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return f'{self.nome}'
    

class Evento(models.Model):
    data = models.DateTimeField(default=timezone.now, verbose_name='Data Início')
    data_termino = models.DateTimeField(default=timezone.now, verbose_name='Data Término*', blank=True, null=True)
    
    nome = models.CharField(max_length=300, default='', verbose_name='Nome')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, verbose_name='Categoria do Evento', blank=True, null=True)

    slug = models.SlugField(default='', max_length=255, verbose_name="Slug", unique=True)
    codigo = models.CharField(max_length=255, default='', verbose_name='Código')

    descricao = models.TextField(max_length=10000, default='', verbose_name='Descrição')
    tipo = models.CharField(
        default='Presencial',
        max_length=255, 
        verbose_name="Tipo", 
        choices=[
            ("Presencial", "Presencial"),
            ("Online", "Online"),
        ],
    )
    pagamento = models.CharField(
        default='Gratuito',
        max_length=255, 
        verbose_name="Pagamento",
        choices=[
            ("Gratuito", "Gratuito"),
            ("Pago", "Pago"),
        ],
    )
    
    valor = models.FloatField(default=0, verbose_name='Valor Geral*', 
                              help_text="""
                              Se o evento for gratuito, desconsidere esse campo e os 3 de baixo.
                              Se o evento for pago, preencha esse campo e fique atento aos detalhes.
                              Apenas se o preço for igual para todos os gêneros.
                              Se você for fazer divisão de preço de acordo com o gênero, 
                              deixe esse campo como 0 e preencha os 3 campos abaixo.
                              """)
    valor_homem = models.FloatField(default=0, verbose_name='Valor Homem*', help_text='Caso não queira essa opção, deixe como 0')
    valor_mulher = models.FloatField(default=0, verbose_name='Valor Mulher*', help_text='Caso não queira essa opção, deixe como 0')
    valor_crianca = models.FloatField(default=0, verbose_name='Valor Criança*', help_text='Caso não queira essa opção, deixe como 0')
    presenca_crianca = models.BooleanField(default=False, verbose_name='O evento pode ter criança?', 
                                              help_text='Marque se o evento pode ter criança ou não')
    idade_crianca = models.IntegerField(default=12, verbose_name='Idade Máxima da Criança*', 
                                     help_text='Marque apenas se o evento for ter criança. Ex: 12 anos')

    maximo_participantes = models.IntegerField(default=1, verbose_name='Máximo de Participantes')
    qtd_participantes = models.IntegerField(default=1, verbose_name='Quantidade')
    qtd_participantes_homens = models.IntegerField(default=1, verbose_name='Quantidade Homem')
    qtd_participantes_mulheres = models.IntegerField(default=1, verbose_name='Quantidade Mulher')

    visibilidade = models.BooleanField(default=True, verbose_name='Visibilidade')

    foto = models.ImageField(blank=True, null=True, upload_to='eventos_fotos/%Y/%m/%d', verbose_name="Foto principal")
    video = models.URLField(blank=True, null=True, max_length=2000, verbose_name="Link vídeo*", 
                            help_text='Link do youtube: vá em compartilhar -> incorporar -> pegue o link dentro de "src"')
    video2 = models.FileField(blank=True, null=True, upload_to='eventos_videos/%Y/%m/%d', verbose_name="Arquivo de vídeo*", 
                              help_text='Arquivo de vídeo. Evite vídeos com mais de 100mb, para evitar vídeos pesados no sistema')

    duracao_tipo = models.CharField(
        default='minutos',
        max_length=255, 
        verbose_name="Tipo da Duração", 
        choices=[
            ("minutos", "minutos"),
            ("horas", "horas"),
            ("dias", "dias"),
        ],
    )
    duracao_numero = models.IntegerField(default=0, verbose_name='Duração (Número)')

    divisao_genero = models.CharField(
        default='nenhum',
        max_length=255, 
        verbose_name="Divisão de Gênero", 
        choices=[
            ("nenhum", "nenhum"),
            ("metade", "metade"),
            ("homem", "homem"),
            ("mulher", "mulher"),
        ],
        help_text="""
        Essa opção divide os ingressos para só mulheres, só homens ou divide na metade, em 50%.
        Se não quiser dividir por gênero, deixe marcado como "nenhum".
        """
    )

    # Configurações Gerais para Eventos Online
    link_reuniao = models.CharField(max_length=3000, default='', verbose_name='Link Reunião*', blank=True, null=True, 
                                    help_text='Apenas se o evento for online')

    # Configurações Gerais para Eventos Presenciais
    localizacao = models.CharField(max_length=1000, default='', verbose_name='Localização*', blank=True, null=True, 
                                   help_text='Localização do evento em si')
    link_localizacao = models.URLField(max_length=3000, default='', verbose_name='Link Localização*', blank=True, null=True, 
                                       help_text='LINK GOOGLE MAPS')

    localizacao_inicio = models.CharField(max_length=1000, default='', verbose_name='Localização Início*', blank=True, null=True, 
                                          help_text='Ponto de partida')
    link_localizacao_inicio = models.URLField(max_length=3000, default='', verbose_name='Link Localização Início*', blank=True, null=True,
                                              help_text='LINK GOOGLE MAPS')


    permanencia_noturna = models.BooleanField(default=False, verbose_name='Permanência noturna', 
                                              help_text='As pessoas vão dormir no evento?')

    faixa_etaria = models.CharField(max_length=100, default='', verbose_name='Faixa Etária*', blank=True, null=True, 
                                    help_text='Ex: 18 - 50 anos')

    galeria = models.OneToOneField(GaleriaEvento, on_delete=models.SET_NULL, verbose_name='Galeria', blank=True, null=True, 
                                   help_text="""Primeiro, crie uma galeria de fotos para o evento e adicione aqui. Você pode escolher
                                   até 5 fotos""")
    
    itens_inclusos = models.ManyToManyField(Item, verbose_name='Itens Inclusos*', related_name='itens_inclusos', blank=True)
    itens_exclusos = models.ManyToManyField(Item, verbose_name='Itens NÃO Inclusos*', related_name='itens_exclusos', blank=True)

    info_guia_turistico = models.TextField(max_length=10000, default='', verbose_name='Informação Guia Turístico" *', blank=True, null=True)

    lugares_visitas = models.ManyToManyField(Lugar, verbose_name='Lugares*', related_name='lugares', blank=True, 
                                             help_text='Lugares que serão visitados')
    
    detalhes_dias = models.ManyToManyField(DetalheDia, verbose_name='Detalhes dos dias*', related_name='detalhes_dias', blank=True, 
                                             help_text='Explique os detalhes dos dias do evento')
    
    pergunta = models.ManyToManyField(PerguntaFrequente, verbose_name='Perguntas Frequentes*', related_name='perguntas', blank=True, 
                                             help_text='Coloque a pergunta frequente e explique com detalhes a sua resposta')

    # Informações gerais
    mensagem_motivo = models.TextField(max_length=10000, default='', verbose_name='Campo "por que ir para o evento?" *', blank=True, null=True, 
                                       help_text='Explique o motivo do por quê as pessoas deveriam ir para o evento')
    mensagem_administrador = models.TextField(max_length=10000, default='', verbose_name='Nota do administrador*', blank=True, null=True, 
                                              help_text='Escreva uma mensagem/observação do administrador do evento')

    contato1 = models.CharField(max_length=1000, default='', verbose_name='Contato 1*', blank=True, null=True, help_text='Ex: +44 7911 123456')
    contato2 = models.CharField(max_length=1000, default='', verbose_name='Contato 2*', blank=True, null=True, help_text='Ex: +44 7911 123456')
    
    def get_qtd_vagas(self):
        if self.divisao_genero != 'metade':
            return self.qtd_participantes
        else:
            return f'H:{self.qtd_participantes_homens}/M:{self.qtd_participantes_mulheres}'
    get_qtd_vagas.short_description = 'QTD de Vagas'

    def save(self, *args, **kwargs):
        if self.codigo and Evento.objects.filter(slug=self.slug).exists():
            evento_atual = Evento.objects.get(slug=self.slug)
        else:
            evento_atual = None

        if not self.codigo:
            if self.maximo_participantes and self.divisao_genero != 'metade':
                self.qtd_participantes = self.maximo_participantes
            if self.maximo_participantes and self.divisao_genero == 'metade':
                self.qtd_participantes = self.maximo_participantes
                self.qtd_participantes_homens = int(self.maximo_participantes / 2)
                self.qtd_participantes_mulheres = int(self.maximo_participantes / 2)

            # Gerando Código - Início
            letras = string.ascii_letters
            digitos = string.digits
            # caracteres = '!@#$%&*._-'

            geral = letras + digitos
            while True:
                codigo = ''.join(random.choices(geral, k=25))
                if not Evento.objects.filter(codigo=codigo).exists():
                    break
            # Gerando Código - Fim

            self.codigo = codigo
        else:
            qtd_maxima_antiga = evento_atual.maximo_participantes

            if qtd_maxima_antiga != self.maximo_participantes:
                diferenca = self.maximo_participantes - qtd_maxima_antiga

                if evento_atual and self.divisao_genero != 'metade':
                    self.qtd_participantes += diferenca
                elif evento_atual and self.divisao_genero == 'metade':
                    self.qtd_participantes += diferenca
                    self.qtd_participantes_homens += int(diferenca / 2)
                    self.qtd_participantes_mulheres += int(diferenca / 2)

        if self.nome:
            slug_formatada = f'{self.nome}-{self.codigo}'
            self.slug = f'{slugify(slug_formatada)}'

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f'{self.nome}'
    

# Configurações Evento - Fim


class ParticipantesEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name='Evento')
    remetente = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='participantes_evento_remetentes', verbose_name='Remetente')
    confirmacao = models.CharField(
        default='Pendente',
        max_length=255, 
        verbose_name="Confirmação", 
        choices=[
            ("Pendente", "Pendente"),
            ("Rejeitado", "Rejeitado"),
            ("Confirmado", "Confirmado"),
        ],
    )

    comparecer_evento = models.CharField(
        default='Pendente',
        max_length=255, 
        verbose_name="Apareceu no evento?", 
        choices=[
            ("Pendente", "Pendente"),
            ("Confirmado", "Confirmado"),
        ],
    )


    bilhete = models.FileField(verbose_name='Bilhete', blank=True, null=True, upload_to='bilhetes/%Y/%m/%d')
    codigo = models.CharField(default='', max_length=1000, verbose_name='Código', blank=True, null=True)
    link_confirmacao = models.URLField(default='', verbose_name='Link Confirmação', blank=True, null=True)
    img_qrcode = models.ImageField(upload_to='qr_code/%Y/%m/%d', verbose_name='QR Code', blank=True, null=True)

    class Meta:
        verbose_name = 'Participante Evento'
        verbose_name_plural = 'Participantes Evento'

    def __str__(self):
        return f'{self.evento} - {self.remetente} - {self.confirmacao}'



class ConviteEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name='Evento')

    remetente = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='convite_evento_remetentes', verbose_name='Remetente')
    destinatario = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='convite_evento_destinatario', verbose_name='Destinatário')
    confirmacao = models.CharField(
        default='Pendente',
        max_length=255, 
        verbose_name="Confirmação", 
        choices=[
            ("Pendente", "Pendente"),
            ("Rejeitado", "Rejeitado"),
            ("Confirmado", "Confirmado"),
        ],
    )

    descricao = models.TextField(max_length=2000, default='', verbose_name='Descrição', blank=True, null=True)

    class Meta:
        verbose_name = 'Convite Evento'
        verbose_name_plural = 'Convite Evento'

    def __str__(self):
        return f'{self.remetente} -> {self.destinatario}'


class Notificacao(models.Model):
    tipo = models.CharField(
        default='Evento',
        max_length=255, 
        verbose_name="Tipo", 
        choices=[
            ("Evento", "Evento"),
            ("Chamada Video", "Chamada Video"),
        ],
    )

    convite_evento = models.ForeignKey(ConviteEvento, on_delete=models.CASCADE, verbose_name='Convite Evento', blank=True, null=True)
    video_chamada = models.ForeignKey(VideoChamada, on_delete=models.CASCADE, verbose_name='Vídeo Chamada', blank=True, null=True)

    confirmacao = models.CharField(
        default='Pendente',
        max_length=255, 
        verbose_name="Confirmação", 
        choices=[
            ("Pendente", "Pendente"),
            ("Rejeitado", "Rejeitado"),
            ("Confirmado", "Confirmado"),
        ],
    )

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return f'{self.id} - {self.tipo}'
    

