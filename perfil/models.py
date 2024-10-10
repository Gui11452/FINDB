from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify
import string
import random
from namoro.settings import DOMINIO


class Cupido(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome", unique=True)
    email = models.EmailField(max_length=255, verbose_name="Email")
    pais = models.CharField(
        default='Alemanha',
        max_length=255, 
        verbose_name="País", 
        choices=[
            ("Alemanha", "Alemanha"),
            ("Áustria", "Áustria"),
            ("Bélgica", "Bélgica"),
            ("Bulgária", "Bulgária"),
            ("Chipre", "Chipre"),
            ("Croácia", "Croácia"),
            ("Dinamarca", "Dinamarca"),
            ("Eslováquia", "Eslováquia"),
            ("Eslovênia", "Eslovênia"),
            ("Espanha", "Espanha"),
            ("Estônia", "Estônia"),
            ("Finlândia", "Finlândia"),
            ("França", "França"),
            ("Grécia", "Grécia"),
            ("Hungria", "Hungria"),
            ("Irlanda", "Irlanda"),
            ("Itália", "Itália"),
            ("Letônia", "Letônia"),
            ("Lituânia", "Lituânia"),
            ("Luxemburgo", "Luxemburgo"),
            ("Malta", "Malta"),
            ("Países Baixos", "Países Baixos"),
            ("Polônia", "Polônia"),
            ("Portugal", "Portugal"),
            ("Romênia", "Romênia"),
            ("Suécia", "Suécia"),
            ("Albânia", "Albânia"),
            ("Andorra", "Andorra"),
            ("Armênia", "Armênia"),
            ("Azerbaijão", "Azerbaijão"),
            ("Bielorrússia", "Bielorrússia"),
            ("Bósnia e Herzegovina", "Bósnia e Herzegovina"),
            ("Cazaquistão", "Cazaquistão"),
            ("Geórgia", "Geórgia"),
            ("Islândia", "Islândia"),
            ("Kosovo", "Kosovo"),
            ("Liechtenstein", "Liechtenstein"),
            ("Moldávia", "Moldávia"),
            ("Mônaco", "Mônaco"),
            ("Montenegro", "Montenegro"),
            ("Macedônia do Norte", "Macedônia do Norte"),
            ("Noruega", "Noruega"),
            ("Rússia", "Rússia"),
            ("San Marino", "San Marino"),
            ("Sérvia", "Sérvia"),
            ("Suíça", "Suíça"),
            ("Turquia", "Turquia"),
            ("Ucrânia", "Ucrânia"),
            ("Reino Unido", "Reino Unido"),
            ("Vaticano", "Vaticano"),
        ],
    )
    cidade = models.CharField(max_length=255, default='', verbose_name='Cidade', blank=True, null=True)

    slug = models.SlugField(default='', max_length=255, verbose_name="Slug", unique=True)
    codigo = models.CharField(max_length=255, default='', verbose_name='Código', unique=True)
    link = models.URLField(max_length=1000, default='', verbose_name='Link')
    foto = models.ImageField(blank=True, null=True, upload_to='fotos/%Y/%m/%d', verbose_name="Foto")

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário", blank=True, null=True)

    def clean(self, *args, **kwargs):
        error_messages = {}

        if Cupido.objects.filter(nome=self.nome).exists():
            error_messages['nome'] = 'Esse nome já existe como cupido. Por favor, mude para outro.'

        if Cupido.objects.filter(email=self.email).exists():
            error_messages['email'] = 'Esse e-mail já está atrelado a um cupido como cupido. Por favor, mude para outro.'

        if error_messages:
            raise ValidationError(error_messages)

    def save(self, *args, **kwargs):
        if not self.codigo:
            # Gerando Código - Início
            letras = string.ascii_letters
            digitos = string.digits
            # caracteres = '!@#$%&*._-'

            geral = letras + digitos

            while True:
                codigo = ''.join(random.choices(geral, k=25))
                if not Cupido.objects.filter(codigo=codigo).exists():
                    break
            # Gerando Código - Fim

            self.codigo = codigo
            self.link = f'{DOMINIO}/perfil/registrar_conta/{codigo}/'

        if self.nome:
            slug_formatada = f'{self.nome}-{self.codigo}'
            self.slug = f'{slugify(slug_formatada)}'

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cupido'
        verbose_name_plural = 'Cupidos'

    def __str__(self):
        return f'{self.nome}'


class ColaboradoresEvento(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome", unique=True)
    pais = models.CharField(
        default='Alemanha',
        max_length=255, 
        verbose_name="País", 
        choices=[
            ("Alemanha", "Alemanha"),
            ("Áustria", "Áustria"),
            ("Bélgica", "Bélgica"),
            ("Bulgária", "Bulgária"),
            ("Chipre", "Chipre"),
            ("Croácia", "Croácia"),
            ("Dinamarca", "Dinamarca"),
            ("Eslováquia", "Eslováquia"),
            ("Eslovênia", "Eslovênia"),
            ("Espanha", "Espanha"),
            ("Estônia", "Estônia"),
            ("Finlândia", "Finlândia"),
            ("França", "França"),
            ("Grécia", "Grécia"),
            ("Hungria", "Hungria"),
            ("Irlanda", "Irlanda"),
            ("Itália", "Itália"),
            ("Letônia", "Letônia"),
            ("Lituânia", "Lituânia"),
            ("Luxemburgo", "Luxemburgo"),
            ("Malta", "Malta"),
            ("Países Baixos", "Países Baixos"),
            ("Polônia", "Polônia"),
            ("Portugal", "Portugal"),
            ("Romênia", "Romênia"),
            ("Suécia", "Suécia"),
            ("Albânia", "Albânia"),
            ("Andorra", "Andorra"),
            ("Armênia", "Armênia"),
            ("Azerbaijão", "Azerbaijão"),
            ("Bielorrússia", "Bielorrússia"),
            ("Bósnia e Herzegovina", "Bósnia e Herzegovina"),
            ("Cazaquistão", "Cazaquistão"),
            ("Geórgia", "Geórgia"),
            ("Islândia", "Islândia"),
            ("Kosovo", "Kosovo"),
            ("Liechtenstein", "Liechtenstein"),
            ("Moldávia", "Moldávia"),
            ("Mônaco", "Mônaco"),
            ("Montenegro", "Montenegro"),
            ("Macedônia do Norte", "Macedônia do Norte"),
            ("Noruega", "Noruega"),
            ("Rússia", "Rússia"),
            ("San Marino", "San Marino"),
            ("Sérvia", "Sérvia"),
            ("Suíça", "Suíça"),
            ("Turquia", "Turquia"),
            ("Ucrânia", "Ucrânia"),
            ("Reino Unido", "Reino Unido"),
            ("Vaticano", "Vaticano"),
        ],
    )
    regiao = models.CharField(max_length=255, default='', verbose_name='Região', blank=True)
    celular = models.CharField(max_length=500, default='', verbose_name='Celular', blank=True)

    slug = models.SlugField(default='', max_length=255, verbose_name="Slug", unique=True)
    codigo = models.CharField(max_length=255, default='', verbose_name='Código', unique=True)
    foto = models.ImageField(blank=True, null=True, upload_to='fotos/%Y/%m/%d', verbose_name="Foto")

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")

    def clean(self, *args, **kwargs):
        error_messages = {}

        if ColaboradoresEvento.objects.filter(nome=self.nome).exists():
            error_messages['nome'] = 'Esse nome já existe como cupido. Por favor, mude para outro.'

        if ColaboradoresEvento.objects.filter(email=self.email).exists():
            error_messages['email'] = 'Esse e-mail já está atrelado a um cupido como cupido. Por favor, mude para outro.'

        if error_messages:
            raise ValidationError(error_messages)

    def save(self, *args, **kwargs):
        if not self.codigo:
            # Gerando Código - Início
            letras = string.ascii_letters
            digitos = string.digits
            # caracteres = '!@#$%&*._-'

            geral = letras + digitos

            while True:
                codigo = ''.join(random.choices(geral, k=25))
                if not ColaboradoresEvento.objects.filter(codigo=codigo).exists():
                    break
            # Gerando Código - Fim

            self.codigo = codigo

        if self.nome:
            slug_formatada = f'{self.nome}-{self.codigo}'
            self.slug = f'{slugify(slug_formatada)}'

        return super().save(*args, **kwargs)

    def get_email(self):
        return self.usuario.email
    get_email.short_description = 'E-mail'

    class Meta:
        verbose_name = 'Colaborador Evento'
        verbose_name_plural = 'Colaboradores Evento'

    def __str__(self):
        return f'{self.nome}'



class Perfil(models.Model):
    cupido = models.ForeignKey(Cupido, on_delete=models.SET_NULL, verbose_name="Cupido", blank=True, null=True)

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    slug = models.SlugField(default='', max_length=255, verbose_name="Slug", unique=True)

    genero = models.CharField(
        default='Masculino',
        max_length=255, 
        verbose_name="Gênero", 
        choices=[
            ("Masculino", "Masculino"),
            ("Feminino", "Feminino"),
            ("Outros", "Outros"),
        ],
    )
    aniversario = models.DateField(default=timezone.now, verbose_name="Aniversário")
    idade = models.IntegerField(default=0, verbose_name='Idade')

    nacionalidade = models.CharField(max_length=255, verbose_name="Nacionalidade")

    pais = models.CharField(
        default='Alemanha',
        max_length=255, 
        verbose_name="País", 
        choices=[
            ("Alemanha", "Alemanha"),
            ("Áustria", "Áustria"),
            ("Bélgica", "Bélgica"),
            ("Bulgária", "Bulgária"),
            ("Chipre", "Chipre"),
            ("Croácia", "Croácia"),
            ("Dinamarca", "Dinamarca"),
            ("Eslováquia", "Eslováquia"),
            ("Eslovênia", "Eslovênia"),
            ("Espanha", "Espanha"),
            ("Estônia", "Estônia"),
            ("Finlândia", "Finlândia"),
            ("França", "França"),
            ("Grécia", "Grécia"),
            ("Hungria", "Hungria"),
            ("Irlanda", "Irlanda"),
            ("Itália", "Itália"),
            ("Letônia", "Letônia"),
            ("Lituânia", "Lituânia"),
            ("Luxemburgo", "Luxemburgo"),
            ("Malta", "Malta"),
            ("Países Baixos", "Países Baixos"),
            ("Polônia", "Polônia"),
            ("Portugal", "Portugal"),
            ("Romênia", "Romênia"),
            ("Suécia", "Suécia"),
            ("Albânia", "Albânia"),
            ("Andorra", "Andorra"),
            ("Armênia", "Armênia"),
            ("Azerbaijão", "Azerbaijão"),
            ("Bielorrússia", "Bielorrússia"),
            ("Bósnia e Herzegovina", "Bósnia e Herzegovina"),
            ("Cazaquistão", "Cazaquistão"),
            ("Geórgia", "Geórgia"),
            ("Islândia", "Islândia"),
            ("Kosovo", "Kosovo"),
            ("Liechtenstein", "Liechtenstein"),
            ("Moldávia", "Moldávia"),
            ("Mônaco", "Mônaco"),
            ("Montenegro", "Montenegro"),
            ("Macedônia do Norte", "Macedônia do Norte"),
            ("Noruega", "Noruega"),
            ("Rússia", "Rússia"),
            ("San Marino", "San Marino"),
            ("Sérvia", "Sérvia"),
            ("Suíça", "Suíça"),
            ("Turquia", "Turquia"),
            ("Ucrânia", "Ucrânia"),
            ("Reino Unido", "Reino Unido"),
            ("Vaticano", "Vaticano"),
        ],
    )

    celular = models.CharField(max_length=255, verbose_name="Celular")
    regiao = models.CharField(max_length=255, verbose_name="Região")
    interesse = models.CharField(
        default='Relacionamento Sério',
        max_length=255, 
        verbose_name="Interesses", 
        choices=[
            ("Networking e Negocios", "Networking e Negocios"),
            ("Terapias diversas", "Terapias diversas"),
            ("Profissionais em relacionamento", "Profissionais em relacionamento"),
            ("Eventos", "Eventos"),
            ("Relacionamento Sério", "Relacionamento Sério"),
            ("Encontros", "Encontros"),
            ("Namoros", "Namoros"),
            ("Amizades", "Amizades")
        ],
    )

    orientacao_sexual = models.CharField(
        default='Heterossexual',
        max_length=255, 
        verbose_name="Orientação Sexual", 
        choices=[
            ("Heterossexual", "Heterossexual"),
            ("Homossexual", "Homossexual"),
            ("Bissexual", "Bissexual"),
            ("Pansexual", "Pansexual"),
            ("Assexual", "Assexual"),
            ("Outros ", "Outros"),
        ],
    )
    profissao = models.CharField(max_length=255, verbose_name="Profissão")

    estado_civil = models.CharField(
        default='Solteiro',
        max_length=255, 
        verbose_name="Estado Civil", 
        choices=[
            ("Solteiro", "Solteiro"),
            ("Casado", "Casado"),
            ("Divorciado", "Divorciado"),
            ("Viúvo", "Viúvo"),
            ("Separado", "Separado"),
            ("Relacionamento Sério", "Relacionamento Sério"),
        ],
    )

    signo = models.CharField(
        default='Áries',
        max_length=255, 
        verbose_name="Signo", 
        choices=[
            ("Áries", "Áries"),
            ("Touro", "Touro"),
            ("Gêmeos", "Gêmeos"),
            ("Câncer", "Câncer"),
            ("Leão", "Leão"),
            ("Virgem", "Virgem"),
            ("Libra", "Libra"),
            ("Escorpião", "Escorpião"),
            ("Sagitário", "Sagitário"),
            ("Capricórnio", "Capricórnio"),
            ("Aquário", "Aquário"),
            ("Peixes", "Peixes"),
        ],
    )

    etnia = models.CharField(
        default='Branco',
        max_length=255, 
        verbose_name="Etnia", 
        choices=[
            ("Branco", "Branco"),
            ("Negro", "Negro"),
            ("Pardo", "Pardo"),
            ("Indígena", "Indígena"),
            ("Amarelo", "Amarelo"),
            ("Outros", "Outros"),
        ],
    )

    cor_cabelo = models.CharField(
        default='Preto',
        max_length=255, 
        verbose_name="Cor do Cabelo", 
        choices=[
            ("Preto", "Preto"),
            ("Castanho", "Castanho"),
            ("Loiro", "Loiro"),
            ("Ruivo", "Ruivo"),
            ("Grisalho", "Grisalho"),
            ("Outros", "Outros"),
        ],
    )

    cor_olhos = models.CharField(
        default='Azul',
        max_length=255, 
        verbose_name="Cor dos Olhos", 
        choices=[
            ("Azul", "Azul"),
            ("Verde", "Verde"),
            ("Castanho", "Castanho"),
            ("Preto", "Preto"),
            ("Outro", "Outro"),
        ],
    )

    altura = models.CharField(
        default='Abaixo de 1,50m',
        max_length=255, 
        verbose_name="Altura", 
        choices=[
            ("Abaixo de 1,50m", "Abaixo de 1,50m"),
            ("1,50m - 1,60m", "1,50m - 1,60m"),
            ("1,60m - 1,70m", "1,60m - 1,70m"),
            ("1,70m - 1,80m", "1,70m - 1,80m"),
            ("1,80m - 1,90m", "1,80m - 1,90m"),
            ("Mais de 1,90m", "Mais de 1,90m"),
        ],
    )

    tipo_corpo = models.CharField(
        default='Magro',
        max_length=255, 
        verbose_name="Tipo do Corpo", 
        choices=[
            ("Magro", "Magro"),
            ("Normal", "Normal"),
            ("Atlético", "Atlético"),
            ("Gordo", "Gordo"),
            ("Musculoso", "Musculoso"),
            ("Outros", "Outros"),
        ],
    )

    fuma = models.CharField(
        default='Sim',
        max_length=255, 
        verbose_name="Fuma?", 
        choices=[
            ("Sim", "Sim"),
            ("Não", "Não"),
        ],
    )

    bebe = models.CharField(
        default='Sim',
        max_length=255, 
        verbose_name="Bebe?", 
        choices=[
            ("Sim", "Sim"),
            ("Não", "Não"),
        ],
    )

    descricao = models.TextField(max_length=10000, verbose_name="Descrição")

    foto = models.ImageField(blank=True, null=True, upload_to='fotos/%Y/%m/%d', verbose_name="Foto")

    verificacao_email = models.BooleanField(default=False, verbose_name='Verificação E-mail')
    codigo = models.CharField(max_length=255, default='', verbose_name='Código')
    codigo_cancelar_assinatura = models.CharField(max_length=255, default='', verbose_name='Código C.A', blank=True, null=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    def get_email(self):
        return self.usuario.email
    get_email.short_description = 'E-mail'

    def save(self, *args, **kwargs):
        if not self.usuario.username or not self.codigo:
            # Gerando Código - Início
            letras = string.ascii_letters
            digitos = string.digits
            geral = letras + digitos
            while True:
                codigo = ''.join(random.choices(geral, k=25))
                if not Perfil.objects.filter(codigo=codigo, usuario__username=codigo).exists():
                    break
            # Gerando Código - Fim
            self.usuario.username = codigo
            self.codigo = codigo

        if self.nome:
            slug_formatada = f'{self.nome}-{self.usuario.username}'
            self.slug = f'{slugify(slug_formatada)}'

        if self.aniversario:
            ano_data_atual = int(datetime.now().strftime('%Y'))
            ano_nascimento = int(self.aniversario.strftime('%Y'))

            self.idade = ano_data_atual - ano_nascimento

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'{self.nome}'



class Album(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, verbose_name="Perfil")
    foto1 = models.ImageField(blank=True, null=True, upload_to='album/%Y/%m/%d', verbose_name="Foto 1")
    foto2 = models.ImageField(blank=True, null=True, upload_to='album/%Y/%m/%d', verbose_name="Foto 2")
    foto3 = models.ImageField(blank=True, null=True, upload_to='album/%Y/%m/%d', verbose_name="Foto 3")
    foto4 = models.ImageField(blank=True, null=True, upload_to='album/%Y/%m/%d', verbose_name="Foto 4")
    foto5 = models.ImageField(blank=True, null=True, upload_to='album/%Y/%m/%d', verbose_name="Foto 5")

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albuns'

    def __str__(self):
        return f'Álbum de {self.perfil.nome}'



class RecuperacaoSenha(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    recuperacao = models.BooleanField(default=False, verbose_name='Foi Recuperado?')
    codigo = models.CharField(max_length=255, default='', verbose_name='Código')
    data = models.DateTimeField(default=timezone.now, verbose_name='Data')

    class Meta:
        verbose_name = 'Recuperação de Senha'
        verbose_name_plural = 'Recuperação de Senhas'

    def __str__(self):
        return f'{self.usuario}'
    

class VideoChamada(models.Model):
    remetente = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='video_chamada_remetente', verbose_name='Remetente')
    destinatario = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='video_chamada_destinatario', verbose_name='Destinatário')
    cupido = models.ForeignKey(Cupido, on_delete=models.CASCADE ,verbose_name='Cupido', blank=True, null=True)
    link_reuniao = models.CharField(max_length=3000, default='', verbose_name='Link Reunião')
    senha_reuniao = models.CharField(max_length=1000, default='', verbose_name='Senha reunião', blank=True, null=True)
    
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

    data = models.DateTimeField(default=timezone.now, verbose_name='Data')
    descricao = models.TextField(max_length=2000, default='', verbose_name='Descrição', blank=True, null=True)

    class Meta:
        verbose_name = 'Video Chamada'
        verbose_name_plural = 'Video Chamadas'

    def __str__(self):
        return f'{self.remetente} -> {self.destinatario}'