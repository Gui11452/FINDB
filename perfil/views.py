from django.shortcuts import render, redirect, reverse
from .models import Perfil, RecuperacaoSenha, Cupido, Album, VideoChamada
from eventos.models import Notificacao, ParticipantesEvento, Evento
from comunication.models import BloquearUsuarios
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from datetime import datetime, timedelta
from django.utils import timezone
import random
from faker import Faker
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import re
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string	
from django.utils.html import strip_tags			
from django.conf import settings
import requests
import base64
import string
import os
import pytz
from eventos.views import get_perfil_notificacoes
from payment.models import Pedido, Plano
from namoro.settings import CLIENT_ID_ZOOM, CLIENT_SECRET_ZOOM, KEY_SECRET_STRIPE, ZEGOCLOUD_VIDEO_API_KEY, ZEGOCLOUD_VIDEO_SERVER_SECRET, DOMINIO
from .utils import get_access_token, schedule_meeting
import stripe
from django.core.validators import validate_email
from PIL import Image
from pprint import pprint


def perfil(request, slug):
    """ if not request.user.is_authenticated:
        return redirect('home') """
    
    if not Perfil.objects.filter(slug=slug, verificacao_email=True).exists():
        return redirect('home')
    
    hoje = datetime.now()
    amanha = hoje + timedelta(days=1)
    amanha = amanha.replace(hour=0, minute=0, second=0, microsecond=0)
    data_formatada_amanha = amanha.strftime('%Y-%m-%dT%H:%M')
    
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')
    
    perfil = Perfil.objects.get(slug=slug, verificacao_email=True)

    pedido = None
    my_perfil = False
    if request.user.is_authenticated:
        if Perfil.objects.filter(usuario=request.user, verificacao_email=True):
            meu_perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
            my_perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

            if perfil.slug != meu_perfil.slug:
                meu_perfil = False
            else:
                # Verificação Pedido - Início
                if Pedido.objects.filter(perfil=perfil).exists():
                    if Pedido.objects.filter(perfil=perfil, status_pedido='approved', plano_ativo=True).exists():
                        pedido = Pedido.objects.get(perfil=perfil, status_pedido='approved', plano_ativo=True)
                    else:
                        pedido = Pedido.objects.get(perfil=perfil)
                # Verificação Pedido - Fim
        else:
            meu_perfil = False
    else:
        meu_perfil = False

    if request.session.get('get_perfil_slug'):
        perfis = Perfil.objects.exclude(slug=request.session.get('get_perfil_slug'))
        perfis = perfis.exclude(interesse='Terapias diversas')
        perfis = perfis.exclude(interesse='Profissionais em relacionamento')
        perfis = perfis.exclude(verificacao_email=False)
    else:
        """ perfis = Perfil.objects.exclude(
            Q(
                Q(interesse='Terapias diversas') |
                Q(interesse='Profissionais em relacionamento'),
            ), 
            verificacao_email=False,
        ) """
        perfis = Perfil.objects.exclude(interesse='Terapias diversas')
        perfis = perfis.exclude(interesse='Profissionais em relacionamento')
        perfis = perfis.exclude(verificacao_email=False)
    if request.user.is_authenticated and Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        _perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

        perfis = perfis.filter(interesse=_perfil.interesse)
        
        if _perfil.interesse == 'Namoros' or _perfil.interesse == 'Relacionamento Sério' or _perfil.interesse == 'Encontros':
            if _perfil.orientacao_sexual == 'Heterossexual' and _perfil.genero == 'Masculino':
                perfis = perfis.filter(
                    Q(
                        Q(orientacao_sexual='Heterossexual') |
                        Q(orientacao_sexual='Bissexual'),
                    ), 
                    genero='Feminino'
                )
            elif _perfil.orientacao_sexual == 'Heterossexual' and _perfil.genero == 'Feminino':
                perfis = perfis.filter(
                    Q(
                        Q(orientacao_sexual='Heterossexual') |
                        Q(orientacao_sexual='Bissexual'),
                    ), 
                    genero='Masculino'
                )
            elif _perfil.orientacao_sexual == 'Homossexual' and _perfil.genero == 'Feminino':
                perfis = perfis.filter(
                    Q(
                        Q(orientacao_sexual='Homossexual') |
                        Q(orientacao_sexual='Bissexual'),
                    ), 
                    genero='Feminino'
                )
            elif _perfil.orientacao_sexual == 'Homossexual' and _perfil.genero == 'Masculino':
                perfis = perfis.filter(
                    Q(
                        Q(orientacao_sexual='Homossexual') |
                        Q(orientacao_sexual='Bissexual'),
                    ), 
                    genero='Masculino'
                )
            elif _perfil.orientacao_sexual == 'Bissexual':
                perfis = perfis.filter(
                    Q(
                        Q(genero='Masculino') |
                        Q(genero='Feminino'),
                    ), 
                    orientacao_sexual='Bissexual'
                )
            elif _perfil.orientacao_sexual == 'Assexual':
                perfis = perfis.filter(orientacao_sexual='Assexual')
    
    if BloquearUsuarios.objects.filter(usuario=my_perfil, bloqueado=perfil).exists():
        bloqueador_perfil = BloquearUsuarios.objects.get(usuario=my_perfil, bloqueado=perfil)
    else:
        bloqueador_perfil = None

    perfis = list(perfis)
    
    for i in range(10):
        random.shuffle(perfis)
    perfis = perfis[:15]

    qtd_fotos = 0
    if Album.objects.filter(perfil=perfil).exists():
        album = Album.objects.get(perfil=perfil)
        if album.foto1:
            qtd_fotos+=1
        if album.foto2:
            qtd_fotos+=1
        if album.foto3:
            qtd_fotos+=1
        if album.foto4:
            qtd_fotos+=1
        if album.foto5:
            qtd_fotos+=1
    else:
        album = None

    cupidos = Cupido.objects.filter(usuario=None)

    if request.method != 'POST':
        return render(request, 'perfil.html', {
            'perfil': perfil,
            'perfis': perfis,
            'meu_perfil': meu_perfil,
            'album': album,
            'qtd_fotos': qtd_fotos,
            'todas_notificacoes': todas_notificacoes,
            'data_formatada_amanha': data_formatada_amanha,
            'pedido': pedido,
            'cupidos': cupidos,
            'bloqueador_perfil': bloqueador_perfil,
        })
    
    if meu_perfil:
        
        foto_perfil = request.FILES.get('foto-perfil', '')
        foto1 = request.FILES.get('foto1', '')
        foto2 = request.FILES.get('foto2', '')
        foto3 = request.FILES.get('foto3', '')
        foto4 = request.FILES.get('foto4', '')
        foto5 = request.FILES.get('foto5', '')
        remover = request.POST.getlist('remover', '')


        if not Album.objects.filter(perfil=perfil).exists():
            album = Album.objects.create(perfil=perfil)
        
        """ if 'foto-perfil' in remover and perfil.foto:
            caminho_imagem = perfil.foto.path
            perfil.foto = None
            os.remove(caminho_imagem)
            perfil.save()

            if Cupido.objects.filter(usuario=perfil.usuario).exists():
                _cupido = Cupido.objects.get(usuario=perfil.usuario)
                if _cupido.foto:
                    caminho_imagem = _cupido.foto.path
                    _cupido.foto = None
                    os.remove(caminho_imagem)
                    _cupido.save() """

        if 'foto1' in remover and album.foto1:
            caminho_imagem = album.foto1.path
            album.foto1 = None
            os.remove(caminho_imagem)
        if 'foto2' in remover and album.foto2:
            caminho_imagem = album.foto2.path
            album.foto2 = None
            os.remove(caminho_imagem)
        if 'foto3' in remover and album.foto3:
            caminho_imagem = album.foto3.path
            album.foto3 = None
            os.remove(caminho_imagem)
        if 'foto4' in remover and album.foto4:
            caminho_imagem = album.foto4.path
            album.foto4 = None
            os.remove(caminho_imagem)
        if 'foto5' in remover and album.foto5:
            caminho_imagem = album.foto5.path
            album.foto5 = None
            os.remove(caminho_imagem)

        # if 'foto-perfil' not in remover and foto_perfil:
        if foto_perfil:
            perfil.foto = foto_perfil
            perfil.save()

            """ if Cupido.objects.filter(usuario=perfil.usuario).exists():
                _cupido = Cupido.objects.get(usuario=perfil.usuario)
                _cupido.foto = foto_perfil
                _cupido.save() """

        if 'foto1' not in remover and foto1:
            album.foto1 = foto1
        if 'foto2' not in remover and foto2:
            album.foto2 = foto2
        if 'foto3' not in remover and foto3:
            album.foto3 = foto3
        if 'foto4' not in remover and foto4:
            album.foto4 = foto4
        if 'foto5' not in remover and  foto5:
            album.foto5 = foto5
    
        album.save()

        messages.success(request, 'O seu álbum foi alterado')
        return render(request, 'perfil.html', {
            'perfil': perfil,
            'perfis': perfis,
            'meu_perfil': meu_perfil,
            'album': album,
            'qtd_fotos': qtd_fotos,
            'todas_notificacoes': todas_notificacoes,
            'data_formatada_amanha': data_formatada_amanha,
            'pedido': pedido,
            'cupidos': cupidos,
            'bloqueador_perfil': bloqueador_perfil,
        })

    else:
        return render(request, 'perfil.html', {
            'perfil': perfil,
            'perfis': perfis,
            'meu_perfil': meu_perfil,
            'album': album,
            'qtd_fotos': qtd_fotos,
            'todas_notificacoes': todas_notificacoes,
            'data_formatada_amanha': data_formatada_amanha,
            'cupidos': cupidos,
            'bloqueador_perfil': bloqueador_perfil,
        })


def meu_perfil(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return redirect('home')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    return redirect(f'{settings.DOMINIO}/perfil/info/{perfil.slug}/')



def cupido(request, slug):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('home')
	)

    if not Cupido.objects.filter(slug=slug).exists():
        return redirect(http_referer)
    
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    hoje = datetime.now()
    amanha = hoje + timedelta(days=1)
    data_formatada_amanha = amanha.strftime('%Y-%m-%d')
    
    """ link_pesquisa = request.build_absolute_uri()
    link_pesquisa = re.sub(r'&p=\d+', '', link_pesquisa)
    request.session['link_pesquisa'] = link_pesquisa
    request.session.save() """
    
    cupido = Cupido.objects.get(slug=slug)

    if cupido.usuario and Perfil.objects.filter(usuario=cupido.usuario, verificacao_email=True):
        slug_usuario = Perfil.objects.get(usuario=cupido.usuario, verificacao_email=True).slug
    else:
        slug_usuario = ''

    indicacoes = Perfil.objects.filter(cupido=cupido, verificacao_email=True)
    qtd = f'{len(indicacoes)} indicações' if len(indicacoes) > 1 else f'{len(indicacoes)} indicação'

    paginator = Paginator(indicacoes, 10)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)
    
    return render(request, 'cupido.html', {
        'cupido': cupido,
        'page_obj': page_obj,
        'slug_usuario': slug_usuario,
        'qtd': qtd,
        'todas_notificacoes': todas_notificacoes,
    })


def filtro(request):
    pesquisa = request.GET.get('pesquisa', '')
    idade = request.GET.get('idade', '')
    pais = request.GET.get('pais', '')
    orientacao_sexual = request.GET.get('orientacao_sexual', '')
    estado_civil = request.GET.get('estado_civil', '')
    signo = request.GET.get('signo', '')
    etnia = request.GET.get('etnia', '')
    cor_cabelo = request.GET.get('cor_cabelo', '')
    cor_olhos = request.GET.get('cor_olhos', '')
    altura = request.GET.get('altura', '')
    tipo_corpo = request.GET.get('tipo_corpo', '')
    fuma = request.GET.get('fuma', '')
    bebe = request.GET.get('bebe', '')

    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    hoje = datetime.now()
    amanha = hoje + timedelta(days=1)
    amanha = amanha.replace(hour=0, minute=0, second=0, microsecond=0)
    data_formatada_amanha = amanha.strftime('%Y-%m-%dT%H:%M')

    link_pesquisa = request.build_absolute_uri()
    link_pesquisa = re.sub(r'&p=\d+', '', link_pesquisa)
    request.session['link_pesquisa'] = link_pesquisa
    request.session.save()

    if request.session.get('get_perfil_slug'):
        perfis = Perfil.objects.exclude(slug=request.session.get('get_perfil_slug'))
        perfis = perfis.exclude(interesse='Terapias diversas')
        perfis = perfis.exclude(interesse='Profissionais em relacionamento')
        perfis = perfis.exclude(verificacao_email=False)
    else:
        """ perfis = Perfil.objects.exclude(
            Q(
                Q(interesse='Terapias diversas') |
                Q(interesse='Profissionais em relacionamento'),
            ), 
            verificacao_email=False,
        ) """
        perfis = Perfil.objects.exclude(interesse='Terapias diversas')
        perfis = perfis.exclude(interesse='Profissionais em relacionamento')
        perfis = perfis.exclude(verificacao_email=False)

    if request.user.is_authenticated and Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        _my_perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
        perfis = perfis.filter(interesse=_my_perfil.interesse)

        if _my_perfil.interesse == 'Namoros' or _my_perfil.interesse == 'Relacionamento Sério' or _my_perfil.interesse == 'Encontros':
            if _my_perfil.orientacao_sexual == 'Heterossexual' and _my_perfil.genero == 'Masculino':
                perfis = perfis.filter(
                    Q(
                        Q(orientacao_sexual='Heterossexual') |
                        Q(orientacao_sexual='Bissexual'),
                    ), 
                    genero='Feminino'
                )
            elif _my_perfil.orientacao_sexual == 'Heterossexual' and _my_perfil.genero == 'Feminino':
                perfis = perfis.filter(
                    Q(
                        Q(orientacao_sexual='Heterossexual') |
                        Q(orientacao_sexual='Bissexual'),
                    ), 
                    genero='Masculino'
                )
            elif _my_perfil.orientacao_sexual == 'Homossexual' and _my_perfil.genero == 'Feminino':
                perfis = perfis.filter(
                    Q(
                        Q(orientacao_sexual='Homossexual') |
                        Q(orientacao_sexual='Bissexual'),
                    ), 
                    genero='Feminino'
                )
            elif _my_perfil.orientacao_sexual == 'Homossexual' and _my_perfil.genero == 'Masculino':
                perfis = perfis.filter(
                    Q(
                        Q(orientacao_sexual='Homossexual') |
                        Q(orientacao_sexual='Bissexual'),
                    ), 
                    genero='Masculino'
                )
            elif _my_perfil.orientacao_sexual == 'Bissexual':
                perfis = perfis.filter(
                    Q(
                        Q(genero='Masculino') |
                        Q(genero='Feminino'),
                    ), 
                    orientacao_sexual='Bissexual'
                )
            elif _my_perfil.orientacao_sexual == 'Assexual':
                perfis = perfis.filter(orientacao_sexual='Assexual')


    cupidos = Cupido.objects.filter(usuario=None)

    if not pesquisa and not idade and not pais and not orientacao_sexual and not estado_civil and not signo and not etnia and not cor_cabelo and not cor_olhos and not altura and not tipo_corpo and not fuma and not bebe:
        """ if len(perfis) == 1:
            qtd = f'{len(perfis)} pessoa encontrada'
        else:
            qtd = f'{len(perfis)} pessoas encontradas'

        paginator = Paginator(perfis, 1)
        page = request.GET.get('p', 1)
        page_obj = paginator.get_page(page) """

        return render(request, 'filtro.html', {
            # 'page_obj': page_obj,
            # 'qtd': qtd,
            'link_pesquisa': link_pesquisa,
            'todas_notificacoes': todas_notificacoes,
            'data_formatada_amanha': data_formatada_amanha,
            'cupidos': cupidos,
        })

    if pesquisa:
        perfis = perfis.filter(
            Q(nome__icontains=pesquisa) 
            #|
		    #Q(usuario__username__icontains=pesquisa), 
        )

    if idade:
        perfis = perfis.filter(idade=int(idade))

    if pais:
        perfis = perfis.filter(pais=pais)

    if orientacao_sexual:
        perfis = perfis.filter(orientacao_sexual=orientacao_sexual)

    if estado_civil:
        perfis = perfis.filter(estado_civil=estado_civil)

    if signo:
        perfis = perfis.filter(signo=signo)

    if etnia:
        perfis = perfis.filter(etnia=etnia)

    if cor_cabelo:
        perfis = perfis.filter(cor_cabelo=cor_cabelo)

    if cor_olhos:
        perfis = perfis.filter(cor_olhos=cor_olhos)

    if altura:
        perfis = perfis.filter(altura=altura)

    if tipo_corpo:
        perfis = perfis.filter(tipo_corpo=tipo_corpo)

    if fuma:
        perfis = perfis.filter(fuma=fuma)

    if bebe:
        perfis = perfis.filter(bebe=bebe)

    if len(perfis) == 1:
        qtd = f'{len(perfis)} pessoa encontrada'
    else:
        qtd = f'{len(perfis)} pessoas encontradas'

    paginator = Paginator(perfis, 15)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'filtro.html', {
        'page_obj': page_obj,
        'qtd': qtd,
        'link_pesquisa': link_pesquisa,
        'todas_notificacoes': todas_notificacoes,
        'data_formatada_amanha': data_formatada_amanha,
        'cupidos': cupidos,
    })



def criar_perfis_fakes(request):
    faker = Faker('pt_BR')

    n = 100
    for i in range(n):
        while True:
            # Gerando Código - Início
            letras = string.ascii_letters
            digitos = string.digits
            geral = letras + digitos
            email = faker.email()

            codigo = ''.join(random.choices(geral, k=25))
            if not Perfil.objects.filter(codigo=codigo, usuario__username=codigo, usuario__email=email).exists():
                break
            # Gerando Código - Fim

        nome = faker.name()
        genero = random.choice(['Masculino', 'Feminino', 'Outros'])
        aniversario = datetime(random.randint(1970, 2004), random.randint(1, 12), random.randint(1, 25))
        nacionalidade = random.choice(['Português', 'Espanhol', 'Alemão', 'Italiano', 'Francês', 'Holandês'])

        paises = [
            "Alemanha",
            "Áustria",
            "Bélgica",
            "Bulgária",
            "Chipre",
            "Croácia",
            "Dinamarca",
            "Eslováquia",
            "Eslovênia",
            "Espanha",
            "Estônia",
            "Finlândia",
            "França",
            "Grécia",
            "Hungria",
            "Irlanda",
            "Itália",
            "Letônia",
            "Lituânia",
            "Luxemburgo",
            "Malta",
            "Países Baixos",
            "Polônia",
            "Portugal",
            "Romênia",
            "Suécia"
        ]
        pais = random.choice(paises)

        celular = faker.phone_number()
        regiao = faker.address()
        interesse = random.choice(['Networking e Negocios', 'Terapias diversas', 'Profissionais em relacionamento', 'Eventos', 'Relacionamento Sério', 'Encontros', 'Namoros', 'Amizades'])

        orientacao_sexual = random.choice(['Heterossexual', 'Homossexual', 'Bissexual', 'Pansexual', 'Assexual', 'Outros'])
        profissao = faker.job()

        estado_civil = random.choice(['Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'Separado', 'Relacionamento Sério'])
        signo = random.choice(['Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'Separado', 'Relacionamento Sério'])
        etnia = random.choice(["Branco", "Negro", "Pardo", "Indígena", "Amarelo", "Outros"])
        cor_cabelo = random.choice(["Preto", "Castanho", "Loiro", "Ruivo", "Grisalho", "Outros"])
        cor_olhos = random.choice(["Azul", "Verde", "Castanho", "Preto", "Outro"])
        altura = random.choice(["Abaixo de 1,50m", "1,50m - 1,60m", "1,60m - 1,70m", "1,70m - 1,80m", "1,80m - 1,90m", "Mais de 1,90m"])
        tipo_corpo = random.choice(["Magro", "Normal", "Atlético", "Gordo", "Musculoso", "Outros"])
        fuma = random.choice(["Sim", "Não"])
        bebe = random.choice(["Sim", "Não"])
        descricao = faker.text(3000)

        if random.randint(1, 12) % 2 == 0:
            verificacao_email = True
        else:
            verificacao_email = False

        user = User.objects.create_user(username=codigo, email=email)
        user.set_password(faker.password())
        user.save()

        obj = Perfil.objects.create(
            usuario=user,
            nome=nome,
            codigo=codigo,
            genero=genero,
            aniversario=aniversario,
            pais=pais,
            nacionalidade=nacionalidade,
            celular=celular,
            regiao=regiao,
            interesse=interesse,
            orientacao_sexual=orientacao_sexual,
            profissao=profissao,
            estado_civil=estado_civil,
            signo=signo,
            etnia=etnia,
            cor_cabelo=cor_cabelo,
            cor_olhos=cor_olhos,
            altura=altura,
            tipo_corpo=tipo_corpo,
            fuma=fuma,
            bebe=bebe,
            descricao=descricao,
            verificacao_email=verificacao_email,
        )
        obj.save()

    return HttpResponse(f'{n} perfis criados!')

""" weights=[3, 1, 1, 1, 1]
for perfil in Perfil.objects.all():
    # interesse = random.choices(interesses, weights, k=1)
    if perfil.interesse == 'Networking':
        # interesse = random.choice(['Networking e Negocios', 'Terapias diversas', 'Profissionais em relacionamento', 'Eventos'])
        perfil.interesse = 'Networking e Negocios'
        perfil.save()

return HttpResponse(f'Perfis atualizados!') """

""" obj_refund = stripe.Refund.create(
    payment_intent='', 
    amount=2040,
    # metadata={}
)
id_refund = obj_refund.get('id')

return HttpResponse(f'id_refund') """
# return HttpResponse(f'{n} perfis criados!')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method != 'POST':
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    lembrar_senha = request.POST.get('lembrar_senha')
    recaptcha = request.POST.get('g-recaptcha-response')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido!')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })

    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    # Final - Recaptcha

    if not User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail enviado NÃO está atrelado a nenhuma conta.')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    usuario = User.objects.get(email=email)

    if not usuario.is_staff and not Perfil.objects.filter(usuario=usuario).exists():
        messages.error(request, 'O e-mail enviado NÃO está atrelado a nenhum perfil. Fale com o suporte')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    if not usuario.is_staff and Perfil.objects.filter(usuario=usuario, verificacao_email=False).exists():
        messages.error(request, 'O seu e-mail ainda NÃO foi confirmado.')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })

    user = auth.authenticate(request, username=usuario.username, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    # Lembrar Senha - Início
    if lembrar_senha:
        # Configura a sessão para durar por um longo período
        request.session.set_expiry(settings.SESSION_COOKIE_AGE * 7)
    else:
        # A sessão expira quando o navegador é fechado ou por um curto periodo
        request.session.set_expiry(settings.SESSION_COOKIE_AGE)
    # Lembrar Senha - Fim

    auth.login(request, user)

    if request.user.is_staff:
        return redirect(f'{DOMINIO}/admin/')

    return redirect('meu_perfil')


def logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method != 'POST':
        return redirect('perfil')
    
    auth.logout(request)
    messages.success(request, 'Usuário desconectado!')
    return redirect('login')


def registro(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method != 'POST':
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    nome = request.POST.get('nome')
    genero = request.POST.get('genero')
    aniversario = request.POST.get('aniversario')
    nacionalidade = request.POST.get('nacionalidade')
    email = request.POST.get('email')
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')
    pais = request.POST.get('pais')
    regiao = request.POST.get('regiao')
    celular = request.POST.get('celular')
    interesse = request.POST.get('interesses')
    orientacao_sexual = request.POST.get('orientacao_sexual')
    profissao = request.POST.get('profissao')
    estado_civil = request.POST.get('estado_civil')
    signo = request.POST.get('signo')
    etnia = request.POST.get('etnia')
    cor_cabelo = request.POST.get('cor_cabelo')
    cor_olhos = request.POST.get('cor_olhos')
    altura = request.POST.get('altura')
    tipo_corpo = request.POST.get('tipo_corpo')
    fuma = request.POST.get('fuma')
    bebe = request.POST.get('bebe')
    descricao = request.POST.get('descricao')
    foto = request.FILES.get('foto', '')
    aceitar_termos = request.POST.get('aceitar-termos', '')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not nome or not genero or not aniversario or not nacionalidade or not email or not pais or not regiao or not celular or not interesse:
        messages.error(request, 'Todos os campos devem ser preenchidos.')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    if not orientacao_sexual or not profissao or not estado_civil or not signo or not etnia or not cor_cabelo or not cor_olhos or not altura:
        messages.error(request, 'Todos os campos devem ser preenchidos.')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    if not tipo_corpo or not fuma or not bebe or not descricao or not senha1 or not senha2:
        messages.error(request, 'Todos os campos devem ser preenchidos.')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    if not foto:
        messages.error(request, 'Enviar uma foto de perfil é obrigatório.')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    if not aceitar_termos:
        messages.error(request, 'Para realizar o cadastro, você precisa aceitar política de privacidade e os termos de condições.')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    # Final - Recaptcha
    
    # Permitindo só imagens - início
    if not foto:
        foto = None
    elif foto.content_type.startswith('image/'):
        try:
            img = Image.open(foto)
            img.verify()  # Verifica se o arquivo é, de fato, uma imagem
        except(IOError, SyntaxError) as e:
            messages.error(request, 'O arquivo enviado não é uma imagem válida!')
            return render(request, 'registro.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })     
    # Permitindo só imagens - Fim


    try:
        aniversario = datetime.strptime(aniversario, '%d/%m/%Y')
    except:
        messages.error(request, 'Digite uma data válida.')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })

    # Vendo se a pessoa tem menos de 18 anos - Início
    dia_aniversario = int(aniversario.strftime('%d'))
    mes_aniversario = int(aniversario.strftime('%m'))
    ano_aniversario = int(aniversario.strftime('%Y'))

    dia_atual = int(datetime.now().strftime('%d'))
    mes_atual = int(datetime.now().strftime('%m'))
    ano_atual = int(datetime.now().strftime('%Y'))

    idade = ano_atual - ano_aniversario
    if mes_atual < mes_aniversario or (mes_atual == mes_aniversario and dia_atual < dia_aniversario):
        idade-=1
    
    if idade < 18:
        messages.error(request, 'Você tem que ter mais de 18 anos para usar o site.')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    # Vendo se a pessoa tem menos de 18 anos - Fim
    
    if len(senha1) < 5:
        messages.error(request, 'As senhas tem que ter no mínimo 5 caracteres!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    """ if len(username) < 4:
        messages.error(request, 'O usuário tem que ter no mínimo 4 caracteres!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        }) """

    if senha1 != senha2:
        messages.error(request, 'As senhas devem ser iguais!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    if User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail enviado já está atrelado a um usuário. Por favor, use outro')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    """ if User.objects.filter(username=username).exists():
        messages.error(request, 'O usuário enviado já está atrelado a um perfil. Por favor, use outro')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        }) """
    
    if request.session.get('codigo_cupido'):
        codigo_cupido = request.session['codigo_cupido']
        if Cupido.objects.filter(codigo=codigo_cupido).exists():
            cupido = Cupido.objects.get(codigo=codigo_cupido)
    else:
        cupido = None

    # Gerando Código - Início
    letras = string.ascii_letters
    digitos = string.digits
    geral = letras + digitos
    while True:
        codigo = ''.join(random.choices(geral, k=25))
        if not Perfil.objects.filter(codigo=codigo, usuario__username=codigo).exists():
            break
    # Gerando Código - Fim
    
    usuario = User.objects.create_user(
        username=codigo,
        email=email,
        first_name=nome,
        password=senha1,
    )
    usuario.save()
    perfil = Perfil.objects.create(
        usuario=usuario,
        nome=nome,
        genero=genero,
        aniversario=aniversario,
        pais=pais,
        nacionalidade=nacionalidade,
        celular=celular,
        regiao=regiao,
        interesse=interesse,
        orientacao_sexual=orientacao_sexual,
        profissao=profissao,
        estado_civil=estado_civil,
        signo=signo,
        etnia=etnia,
        cor_cabelo=cor_cabelo,
        cor_olhos=cor_olhos,
        altura=altura,
        tipo_corpo=tipo_corpo,
        fuma=fuma,
        bebe=bebe,
        descricao=descricao,
        foto=foto,
        cupido=cupido,
    )

    perfil.codigo = codigo
    if foto:
        perfil.foto = foto
    perfil.save()

    # Enviando E-mail - Início
    html_content = render_to_string('emails/confirmacao_email.html', 
    {'nome': perfil.nome, 'link': f'{settings.DOMINIO}/perfil/confirmacao_email/{codigo}/'})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('Confirmação de E-mail - FINDB', text_content, 
    settings.EMAIL_HOST_USER, [email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim
    
    messages.info(request, 'Cadastrado com sucesso! Mas antes, precisamos confirmar a sua conta.')
    messages.info(request, 'O envio do e-mail de confirmação pode levar no máximo alguns minutos. Por favor, aguarde')
    messages.info(request, 'Verifique o seu e-mail e clique no link. Se não achar, vá na caixa de spam.')
    return redirect('login')



def alterar_dados(request):
    if request.user.is_authenticated and Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
        if request.method != 'POST':
            return render(request, 'alterar_dados.html', {
                'perfil': perfil,
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })
        
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        aniversario = request.POST.get('aniversario')
        nacionalidade = request.POST.get('nacionalidade')
        email = request.POST.get('email')
        pais = request.POST.get('pais')
        regiao = request.POST.get('regiao')
        celular = request.POST.get('celular')
        interesse = request.POST.get('interesses')
        orientacao_sexual = request.POST.get('orientacao_sexual')
        profissao = request.POST.get('profissao')
        estado_civil = request.POST.get('estado_civil')
        signo = request.POST.get('signo')
        etnia = request.POST.get('etnia')
        cor_cabelo = request.POST.get('cor_cabelo')
        cor_olhos = request.POST.get('cor_olhos')
        altura = request.POST.get('altura')
        tipo_corpo = request.POST.get('tipo_corpo')
        fuma = request.POST.get('fuma')
        bebe = request.POST.get('bebe')
        descricao = request.POST.get('descricao')
        foto = request.FILES.get('foto', '')
        recaptcha = request.POST.get('g-recaptcha-response')
        
        # Início - Recaptcha
        if not recaptcha:
            messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
            return render(request, 'alterar_dados.html', {
                'perfil': perfil,
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })

        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_BACK,
                'response': recaptcha
            }
        )

        recaptcha_result = recaptcha_request.json()

        if not recaptcha_result.get('success'):
            messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
            return render(request, 'alterar_dados.html', {
                'perfil': perfil,
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })
        # Final - Recaptcha
        
        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'O e-mail enviado já está atrelado a um usuário. Por favor, use outro')
            return render(request, 'alterar_dados.html', {
                'perfil': perfil,
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })
        
        if foto:
            perfil.foto = foto
            """ if Cupido.objects.filter(usuario=perfil.usuario).exists():
                _cupido = Cupido.objects.get(usuario=perfil.usuario)
                _cupido.foto = foto
                _cupido.save() """

        """ if username:
            perfil.usuario.username = username
            perfil.usuario.save() """

        if nome:
            perfil.nome = nome

        if genero:
            perfil.genero = genero

        if aniversario:
            try:
                data_aniversario = datetime.strptime(aniversario, '%d/%m/%Y')
            except:
                messages.error(request, 'Digite uma data válida.')
                return render(request, 'alterar_dados.html', {
                    'perfil': perfil,
                    'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                })
            
            # Vendo se a pessoa tem menos de 18 anos - Início
            dia_aniversario = int(data_aniversario.strftime('%d'))
            mes_aniversario = int(data_aniversario.strftime('%m'))
            ano_aniversario = int(data_aniversario.strftime('%Y'))

            dia_atual = int(datetime.now().strftime('%d'))
            mes_atual = int(datetime.now().strftime('%m'))
            ano_atual = int(datetime.now().strftime('%Y'))

            idade = ano_atual - ano_aniversario

            if mes_atual < mes_aniversario or (mes_atual == mes_aniversario and dia_atual < dia_aniversario):
                idade-=1
            
            if idade < 18:
                messages.error(request, 'Você tem que ter mais de 18 anos para usar o site.')
                return render(request, 'alterar_dados.html', {
                    'perfil': perfil,
                    'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                })
            
            perfil.aniversario = data_aniversario
            
            # Vendo se a pessoa tem menos de 18 anos - Fim

        if nacionalidade:
            perfil.nacionalidade = nacionalidade

        if pais:
            perfil.pais = pais

        if regiao:
            perfil.regiao = regiao

        if celular:
            perfil.celular = celular

        if interesse:
            perfil.interesse = interesse

        if orientacao_sexual:
            perfil.orientacao_sexual = orientacao_sexual

        if profissao:
            perfil.profissao = profissao

        if estado_civil:
            perfil.estado_civil = estado_civil

        if signo:
            perfil.signo = signo

        if etnia:
            perfil.etnia = etnia

        if cor_cabelo:
            perfil.cor_cabelo = cor_cabelo

        if cor_olhos:
            perfil.cor_olhos = cor_olhos

        if altura:
            perfil.altura = altura

        if tipo_corpo:
            perfil.tipo_corpo = tipo_corpo

        if descricao:
            perfil.descricao = descricao

        if fuma:
            perfil.fuma = fuma

        if bebe:
            perfil.bebe = bebe
        
        if email:
            # Gerando Código - Início
            letras = string.ascii_letters
            digitos = string.digits
            # caracteres = '!@#$%&*._-'

            geral = letras + digitos
            while True:
                codigo = ''.join(random.choices(geral, k=25))
                if not Perfil.objects.filter(codigo=codigo).exists():
                    break
            # Gerando Código - Fim

            perfil.codigo = codigo

        perfil.save()

        if email:
            try:
                validate_email(email)
            except:
                messages.error(request, 'E-mail inválido!')
                return render(request, 'alterar_dados.html', {
                    'perfil': perfil,
                    'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
                })

            # Enviando E-mail - Início
            html_content = render_to_string('emails/reconfirmacao_email.html', 
            {'nome': perfil.nome, 'link': f'{settings.DOMINIO}/perfil/reconfirmacao_email/{codigo}/{email}/'})
            text_content = strip_tags(html_content)

            _email = EmailMultiAlternatives('Pedido de Troca de E-mail - FINDB', text_content, 
            settings.EMAIL_HOST_USER, [perfil.usuario.email])
            _email.attach_alternative(html_content, 'text/html')
            _email.send()
            # Enviando E-mail - Fim
            messages.info(request, 'Você pediu para trocar o e-mail. Enviamos um link para você confirmar a troca, no seu e-mail atual. Se caso for preciso, olhe a caixa de spam.')
            messages.info(request, 'O envio do e-mail de recuperação pode levar no máximo alguns minutos. Por favor, aguarde')
            messages.success(request, 'Os seus outros dados foram alterados com sucesso!')
        else:
            messages.success(request, 'Os seus dados foram alterados com sucesso!')
        return redirect('meu_perfil')
    else:
        return redirect('meu_perfil')


def registrar_conta(request, codigo):
    if request.user.is_authenticated:
        messages.info(request, 'Usuário desconectado')
        auth.logout(request)

    request.session['codigo_cupido'] = codigo
    request.session.save()

    return redirect('registro')


def esqueceu_senha(request):
    if request.user.is_authenticated:
        return redirect('meu_perfil')
    
    if request.method != 'POST':
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    email = request.POST.get('email')
    recaptcha = request.POST.get('g-recaptcha-response')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido!')
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })

    if not User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail enviado NÃO está atrelado a nenhuma conta!')
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    user = User.objects.get(email=email)

    if not Perfil.objects.filter(usuario=user, verificacao_email=True).exists():
        messages.error(request, 'O e-mail enviado NÃO está atrelado a nenhum perfil!')
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    
    perfil = Perfil.objects.get(usuario=user, verificacao_email=True)

    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'esqueceu_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })
    # Final - Recaptcha

    # Gerando Código - Início
    letras = string.ascii_letters
    digitos = string.digits
    # caracteres = '!@#$%&*._-'

    geral = letras + digitos

    while True:
        codigo = ''.join(random.choices(geral, k=25))
        if not RecuperacaoSenha.objects.filter(codigo=codigo).exists():
            break
    # Gerando Código - Fim

    recuperacao = RecuperacaoSenha.objects.create(usuario=user, codigo=codigo)
    recuperacao.save()
    
    # Enviando E-mail - Início
    html_content = render_to_string('emails/esqueceu_senha_email.html', 
    {'nome': perfil.nome, 'link': f'{settings.DOMINIO}/perfil/recuperacao_senha/{codigo}/'})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('Recuperação de Senha - FINDB', text_content, 
    settings.EMAIL_HOST_USER, [email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim

    messages.info(request, 'Enviamos um link para o seu e-mail. Acesse ele para você poder trocar a sua senha com segurança.')
    messages.info(request, 'O envio do e-mail de recuperação pode levar no máximo alguns minutos. Por favor, aguarde')
    messages.info(request, 'Verifique o seu e-mail e clique no link. Se não achar, vá na caixa de spam.')
    return render(request, 'esqueceu_senha.html', {
        'validador': True,
    })
    

def recuperacao_senha(request, codigo):
    if request.user.is_authenticated:
        messages.info(request, 'Você está logado. Saia para poder trocar a senha.')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
        })
    
    if not RecuperacaoSenha.objects.filter(codigo=codigo, recuperacao=False).exists():
        messages.info(request, 'Código inválido. Por favor, peça outra recuperação de senha.')
        return redirect('login')
    
    recuperacao = RecuperacaoSenha.objects.get(codigo=codigo, recuperacao=False)
    
    if request.method != 'POST':
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
        })
    
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not senha1 or not senha2:
        messages.error(request, 'Os campos não podem ficar vazios!')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
        })

    if len(senha1) < 5:
        messages.error(request, 'O usuário tem que ter no mínimo 4 caracteres!')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
        })
    
    if senha1 != senha2:
        messages.error(request, 'As senhas tem que ser iguais!')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
        })
    
    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao enviar o comentário! Você é um robô?')
        return render(request, 'recuperacao_senha.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'usuario': recuperacao.usuario,
            'codigo': codigo,
        })
    # Final - Recaptcha

    recuperacao.usuario.set_password(senha1)
    recuperacao.usuario.save()

    recuperacao.recuperacao = True
    recuperacao.save()

    messages.success(request, f'A senha de: "{recuperacao.usuario}" foi trocada!')
    return redirect('login')


def confirmar_email(request, codigo):
    if not Perfil.objects.filter(codigo=codigo, verificacao_email=False).exists():
        return redirect('home')

    perfil = Perfil.objects.get(codigo=codigo, verificacao_email=False)
    perfil.verificacao_email = True
    perfil.save()

    messages.success(request, 'Parabéns, a sua conta foi verificada com sucesso!')
    messages.success(request, 'Agora, faça login para entrar no site')
    return redirect('login')


def reconfirmar_email(request, codigo, email):
    if not Perfil.objects.filter(codigo=codigo).exists():
        return redirect('home')

    perfil = Perfil.objects.get(codigo=codigo)
    usuario = perfil.usuario
    usuario.email = email
    usuario.save()

    try:
        auth.login(request, usuario)
    except:
        ...

    messages.success(request, 'O seu e-mail foi trocado com sucesso!')
    return redirect('meu_perfil')



def convidar(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method != 'POST':
        return redirect('home')
    
    email = request.POST.get('email')

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return redirect('home')

    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if Perfil.objects.filter(usuario__email=email).exists():
        messages.error(request, f'Esse e-mail já está atrelado a uma conta')
        return redirect('home')

    # Verificação da assinatura - Início
    if not Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
        messages.error(request, f'Você não tem nenhuma assinatura ativa. Contrate uma para poder ter acesso a funcionalidade: "Convidar amigos".')
        return redirect('planos')
    # Verificação da assinatura - Fim

    # Verificação da assinatura - Início
    if Pedido.objects.filter(perfil=perfil, plano_ativo=True, plano__nome='tres_meses').exists():
        messages.error(request, f'O plano "Três meses" NÃO tem acesso a funcionalidade: "Convidar amigos". Mude de plano para ter acesso a ela.')
        return redirect('planos')
    # Verificação da assinatura - Fim

    if perfil.usuario.email == email:
        messages.error(request, 'Você não pode convidar você mesmo.')
        return redirect('home')

    if not Cupido.objects.filter(usuario=request.user).exists():
        cupido = Cupido.objects.create(
            usuario=request.user,
            nome=perfil.nome,
            email=perfil.usuario.email,
            foto=perfil.foto,
            pais=perfil.pais,
            cidade=perfil.regiao,
        )
        cupido.save()
    else:
        cupido = Cupido.objects.get(usuario=request.user)


    # Enviando E-mail - Início
    html_content = render_to_string('emails/convite_cupido_email.html', 
    {'link': cupido.link})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('Encontre o Amor da Sua Vida na FINDB! 💖', text_content, 
    settings.EMAIL_HOST_USER, [email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim
    
    return redirect('convite_enviado')


def convite_enviado(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    return render(request, 'convite_enviado.html', {
        'todas_notificacoes': todas_notificacoes,
    })



""" def teste(request):
    client_id = 'RR1LKkWkRa6bGueXQ8KZZA'
    redirect_uri = f'http://localhost:8000/perfil/convite_chamada_video_enviado'

    return redirect(f'https://zoom.us/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}') """

def chamadas_video(request):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not request.user.is_authenticated:
        return redirect('home')

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return redirect('home')
    
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    chamadas_video = VideoChamada.objects.filter(
        Q(remetente=perfil) |
        Q(destinatario=perfil), 
    ).order_by('-data')

    chamadas_video_filtrados = []
    data_atual = datetime.now()
    for chamada_video in chamadas_video:
        if chamada_video.data > data_atual:
            chamadas_video_filtrados.append(chamada_video)

    qtd = len(chamadas_video_filtrados) if chamadas_video_filtrados else 0

    paginator = Paginator(chamadas_video_filtrados, 10)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)

    data_hoje = datetime.now()

    return render(request, 'chamadas_video.html', {
        'page_obj': page_obj,
        'qtd': qtd,
        'todas_notificacoes': todas_notificacoes,
        'data_hoje': data_hoje,
    })


def chamada_video(request, id):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not request.user.is_authenticated:
        return redirect('home')

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return redirect('home')
    
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not VideoChamada.objects.filter(
        Q(remetente=perfil) |
        Q(destinatario=perfil),
        id=id
    ).exists():
        return redirect(http_referer)
    
    chamada_video = VideoChamada.objects.get(
        Q(remetente=perfil) |
        Q(destinatario=perfil),
        id=id
    )

    data_hoje = datetime.now()

    if Notificacao.objects.filter(video_chamada=chamada_video, confirmacao='Pendente').exists():
        notificacao = Notificacao.objects.get(video_chamada=chamada_video, confirmacao='Pendente')
    else:
        notificacao = None

    return render(request, 'chamada_video.html', {
        'chamada_video': chamada_video,
        'todas_notificacoes': todas_notificacoes,
        'notificacao': notificacao,
        'data_hoje': data_hoje,
    })



def confirmar_chamada_video(request, id):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not request.user.is_authenticated:
        return redirect('home')

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return redirect('home')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not VideoChamada.objects.filter(id=id).exists():
        messages.error(request, 'Essa chamada de vídeo não existe')
        return redirect('chamadas_video')
    
    if VideoChamada.objects.filter(id=id, confirmacao='Rejeitado').exists():
        messages.error(request, 'Essa chamada de vídeo já foi rejeitada.')
        return redirect(http_referer)
    
    if VideoChamada.objects.filter(id=id, confirmacao='Confirmado').exists():
        messages.error(request, 'Essa chamada de vídeo já foi confirmada.')
        return redirect(http_referer)
    
    video_chamada = VideoChamada.objects.get(id=id)

    data_hoje = datetime.now()
    if video_chamada.data < data_hoje:
        messages.error(request, 'A data dessa chamada já passou, portanto, expirou.')
        return redirect(http_referer)

    video_chamada.confirmacao = 'Confirmado'
    video_chamada.save()

    if Notificacao.objects.filter(video_chamada=video_chamada).exists():
        notificacao = Notificacao.objects.get(video_chamada=video_chamada)
        notificacao.confirmacao = 'Confirmado'
        notificacao.save()

    # Enviando E-mail - Início
    html_content = render_to_string('emails/convite_chamada_video_confirmado.html', 
    {'nome_destinatario': notificacao.video_chamada.destinatario.nome, 
    'nome_remetente': notificacao.video_chamada.remetente.nome,
    'data': notificacao.video_chamada.data,
    'link_reuniao': notificacao.video_chamada.link_reuniao,
    'link': f'{settings.DOMINIO}/perfil/chamada_video/{notificacao.video_chamada.id}/'})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives(f'"{notificacao.video_chamada.destinatario.nome}" confirmou o seu convite para chamada de vídeo', text_content, 
    settings.EMAIL_HOST_USER, [notificacao.video_chamada.remetente.usuario.email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim

    return redirect(f'{settings.DOMINIO}/perfil/chamada_video/{video_chamada.id}/')



def convite_chamada_video_enviado(request, id):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not VideoChamada.objects.filter(id=id).exists():
        return redirect(http_referer)
    
    video_chamada = VideoChamada.objects.get(id=id)

    return render(request, 'convite_chamada_video_enviado.html', {
        'todas_notificacoes': todas_notificacoes,
        'video_chamada': video_chamada,
    })



def convite_chamada_video(request):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if request.method != 'POST':
        return redirect(http_referer)
    
    if not request.user.is_authenticated:
        return redirect(http_referer)

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return redirect(http_referer)
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    # Verificação da assinatura - Início
    if not Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
        messages.error(request, f'Você não tem nenhuma assinatura ativa. Contrate uma para poder ter acesso a funcionalidade: "Chamada de vídeo".')
        return redirect('planos')
    # Verificação da assinatura - Fim

    hora = request.POST.get('hora')
    slug_cupido = request.POST.get('slug_cupido', '')

    if slug_cupido and slug_cupido != 'Se desejar, selecione um cupido para participar':

        # Verificação da assinatura cupido - Início
        if Pedido.objects.filter(perfil=perfil, plano_ativo=True, plano__nome='tres_meses').exists():
            messages.error(request, f'O plano "Três meses" NÃO tem acesso a funcionalidade: "Pedir ajuda de um cupido". Mude de plano para ter acesso a ela.')
            return redirect('planos')
        # Verificação da assinatura cupido - Fim

        if not Cupido.objects.filter(usuario=None, slug=slug_cupido).exists():
            messages.error(request, f'Esse cupido NÃO pode ser convidado, pois não é um cupido da administração. Por favor, escolha outro')
            return redirect(http_referer)
    
        cupido = Cupido.objects.get(usuario=None, slug=slug_cupido)
    else:
        cupido = None

    data = datetime.fromisoformat(hora)

    hoje = datetime.now()
    amanha = hoje + timedelta(days=1)
    amanha = amanha.replace(hour=0, minute=0, second=0, microsecond=0)
    # data_formatada_amanha = amanha.strftime('%Y-%m-%dT%H:%M')

    if data < amanha:
        messages.error(request, f'Essa data já passou, portanto, é inválida.')
        return redirect('chamadas_video')

    mensagem = request.POST.get('mensagem', '')
    slug_destinatario = request.POST.get('slug_destinatario')

    if not Perfil.objects.filter(slug=slug_destinatario).exists():
        return redirect(http_referer)
    
    destinatario = Perfil.objects.get(slug=slug_destinatario)

    # Verificação bloqueio - Início
    if BloquearUsuarios.objects.filter(usuario=destinatario, bloqueado=perfil).exists():
        messages.error(request, f'Você não pode convidar "{destinatario.nome}", pois você foi bloqueado.')
        return redirect(http_referer)
    # Verificação bloqueio - Fim

    # Impedindo que perfis com certos interesses sejam chamados para vídeos - Início
    if destinatario.interesse == 'Eventos' or destinatario.interesse == 'Terapias diversas' or destinatario.interesse == 'Profissionais em relacionamento':
        messages.error(request, f'Esse usuário NÃO pode ser convidado para uma chamada de vídeo, pois o interesse dele é: "{destinatario.interesse}"')
        return redirect(f'{settings.DOMINIO}/perfil/info/{slug_destinatario}/')
    # Impedindo que perfis com certos interesses sejam chamados para vídeos - Fim


    # Se o destinatário já recusou uma chamada de vídeo sua, você não pode mais convidar ela para outra chamada de vídeo
    if VideoChamada.objects.filter(remetente=perfil, destinatario=destinatario, confirmacao='Rejeitado').exists():
        messages.error(request, f'Você NÃO pode mais convidar "{destinatario.nome}" para uma chamada de vídeo, pois ele(a) já rejeitou um convite seu de chamada de vídeo.')
        return redirect('chamadas_video')

    else:
        video_chamada = VideoChamada.objects.create(remetente=perfil, 
                                                    destinatario=destinatario, 
                                                    confirmacao='Pendente', 
                                                    descricao=mensagem,
                                                    cupido=cupido,
                                                    data=data,)
        # Gerando o link do zoom - Início
        # Gerando senha reunião
        letras = string.ascii_letters
        digitos = string.digits
        geral = letras + digitos
        senha = ''.join(random.choices(geral, k=7))
        # Gerando Código - Fim

        # Convertendo a data para UTC e formatando no padrão ISO 8601
        data_formatada = video_chamada.data.astimezone(pytz.utc).isoformat()

        name = f'Conversa "{perfil.nome}" - "{destinatario.nome}"'
        access_token = get_access_token(CLIENT_ID_ZOOM, CLIENT_SECRET_ZOOM)
        if not access_token:
            messages.error(request, f'Ocorreu algum erro na geração do link do zoom. Fale pro suporte que o erro foi do tipo: "AUTH"')
            return redirect(f'{settings.DOMINIO}/perfil/info/{slug_destinatario}/')
        link_reuniao = schedule_meeting(access_token, senha, name, data_formatada)
        if not link_reuniao:
            messages.error(request, f'Ocorreu algum erro na geração do link do zoom. Fale pro suporte que o erro foi do tipo: "CM"')
            return redirect(f'{settings.DOMINIO}/perfil/info/{slug_destinatario}/')
        # Gerando o link do zoom - Fim

        video_chamada.senha_reuniao = senha
        video_chamada.link_reuniao = link_reuniao
        video_chamada.save()

        if not Notificacao.objects.filter(tipo='Chamada Video', video_chamada=video_chamada).exists():
            notificacao_evento = Notificacao.objects.create(tipo='Chamada Video', video_chamada=video_chamada)
            notificacao_evento.save()

        if not mensagem:
            mensagem = 'vazio'
        # Enviando E-mail - Início
        html_content = render_to_string('emails/convite_chamada_video_email.html', 
        {'nome_destinatario': video_chamada.destinatario.nome, 
         'nome_remetente': video_chamada.remetente.nome,
         'data': video_chamada.data,
         'link_reuniao': video_chamada.link_reuniao,
         'mensagem': mensagem,
        'link': f'{settings.DOMINIO}/perfil/chamada_video/{video_chamada.id}/'})
        text_content = strip_tags(html_content)

        _email = EmailMultiAlternatives('Você recebeu um convite - FINDB', text_content, 
        settings.EMAIL_HOST_USER, [video_chamada.destinatario.usuario.email])
        _email.attach_alternative(html_content, 'text/html')
        _email.send()
        # Enviando E-mail - Fim


        if cupido:
            # Enviando E-mail - Início
            html_content = render_to_string('emails/convite_cupido_chamada_video_email.html', 
            {
            'cupido_nome': cupido.nome,
            'nome_destinatario': video_chamada.destinatario.nome, 
            'nome_remetente': video_chamada.remetente.nome,
            'data': video_chamada.data,
            'link_reuniao': video_chamada.link_reuniao,
            'mensagem': mensagem,
            'link': f'{settings.DOMINIO}/perfil/chamada_video/{video_chamada.id}/'})
            text_content = strip_tags(html_content)

            _email = EmailMultiAlternatives('Cupido, você recebeu um convite para participar de uma chamada de vídeo - FINDB', text_content, 
            settings.EMAIL_HOST_USER, [cupido.email])
            _email.attach_alternative(html_content, 'text/html')
            _email.send()
            # Enviando E-mail - Fim

        return redirect(f'{settings.DOMINIO}/perfil/convite_chamada_video_enviado/{video_chamada.id}/')




def meus_eventos(request):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )
    
    if not request.user.is_authenticated:
        return redirect(http_referer)

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return redirect(http_referer)
    
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
    participacoes = ParticipantesEvento.objects.filter(remetente=perfil, confirmacao='Confirmado')

    participacoes_filtradas = []
    data_atual = datetime.now()
    for participacao in participacoes:
        if data_atual < participacao.evento.data:
            participacoes_filtradas.append(participacao)

    qtd = len(participacoes_filtradas) if participacoes_filtradas else 0

    paginator = Paginator(participacoes_filtradas, 10)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'eventos_perfil.html', {
        'page_obj': page_obj,
        'qtd': qtd,
        'todas_notificacoes': todas_notificacoes,
    })




""" def teste_sucesso(request):
    return HttpResponse() """