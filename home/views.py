from django.shortcuts import render, redirect, get_list_or_404
from perfil.models import Perfil, Cupido
from .models import Carrossel
from django.db.models import Q
import random
from namoro.settings import DOMINIO
from eventos.views import get_perfil_notificacoes
from datetime import datetime, timedelta
import requests
from django.core.paginator import Paginator
from pprint import pprint
from django.contrib import messages
from payment.models import Pedido

def home(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

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

    hoje = datetime.now()
    amanha = hoje + timedelta(days=1)
    amanha = amanha.replace(hour=0, minute=0, second=0, microsecond=0)
    data_formatada_amanha = amanha.strftime('%Y-%m-%dT%H:%M')

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
    

    perfis = list(perfis)
    for i in range(10):
        random.shuffle(perfis)

    perfis = perfis[:15]

    carrossel = Carrossel.objects.all().first()
    c = 0
    if carrossel and carrossel.banner1:
        c+=1
    if carrossel and carrossel.banner2:
        c+=1
    if carrossel and carrossel.banner3:
        c+=1

    cupidos = Cupido.objects.filter(usuario=None)

    return render(request, 'index.html', {
        'perfis': perfis,
        'todas_notificacoes': todas_notificacoes,
        'data_formatada_amanha': data_formatada_amanha,
        'carrossel': carrossel,
        'c': c,
        'cupidos': cupidos,
    })


def home_filtro(request):
    if not request.GET.get('pesquisa'):
        return redirect(f'home')
    else:
        pesquisa = request.GET.get('pesquisa')
        return redirect(f'{DOMINIO}/perfil/filtro/pessoas/?pesquisa={pesquisa}')


def cupidos(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    hoje = datetime.now()
    amanha = hoje + timedelta(days=1)
    amanha = amanha.replace(hour=0, minute=0, second=0, microsecond=0)
    data_formatada_amanha = amanha.strftime('%Y-%m-%dT%H:%M')
    
    perfis_filtrados = []

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

    for perfil in perfis:
        if perfil.cupido:
            perfis_filtrados.append(perfil)

    paginator = Paginator(perfis_filtrados, 10)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)

    cupidos = Cupido.objects.filter(usuario=None)

    return render(request, 'cupidos.html', {
        'page_obj': page_obj,
        'todas_notificacoes': todas_notificacoes,
        'data_formatada_amanha': data_formatada_amanha,
        'cupidos': cupidos,
    })


def profissionais_relacionamento(request):
    """if not request.user.is_authenticated:
        messages.error(request, f'Você precisa estar online para acessar essa área')
        return redirect('home')

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        messages.error(request, f'O seu usuário não está atrelado a nenhum perfil. Por favor, fale com o suporte.')
        return redirect('home')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    # Verificação da assinatura - Início
    if not Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
        messages.error(request, f'Você não tem nenhuma assinatura ativa. Contrate uma para poder ter acesso a funcionalidade: "Profissionais em relacionamento".')
        return redirect('planos')
    # Verificação da assinatura - Fim

    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    response = requests.get('https://m42api.m-21.tech/api/therapists').json()
    response = list(response)

    qtd = len(response) if response else 0
    paginator = Paginator(response, 10)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'profissionais_relacionamento.html', {
        'page_obj': page_obj,
        'qtd': qtd,
        # 'todas_notificacoes': todas_notificacoes,
    })"""
    return redirect('home')


def profissional(request, uid):
    if not request.user.is_authenticated:
        messages.error(request, f'Você precisa estar online para acessar essa área')
        return redirect('home')

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        messages.error(request, f'O seu usuário não está atrelado a nenhum perfil. Por favor, fale com o suporte.')
        return redirect('home')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    # Verificação da assinatura - Início
    if not Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
        messages.error(request, f'Você não tem nenhuma assinatura ativa. Contrate uma para poder ter acesso a funcionalidade: "Profissionais em relacionamento".')
        return redirect('planos')
    # Verificação da assinatura - Fim
    
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    response = requests.get('https://m42api.m-21.tech/api/therapists').json()
    response = list(response)

    terapeuta = None
    for r in response:
        if r.get('uid') == uid:
            terapeuta = r
            break

    return render(request, 'profissional.html', {
        'profissional': terapeuta,
        'todas_notificacoes': todas_notificacoes,
    })