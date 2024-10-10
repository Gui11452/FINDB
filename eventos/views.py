from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.validators import validate_email
from perfil.models import Perfil
from .models import Evento, ParticipantesEvento, ConviteEvento, Notificacao
from comunication.models import BloquearUsuarios
from perfil.models import ColaboradoresEvento
from payment.models import PagamentoEventos
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string	
from django.utils.html import strip_tags			
from django.conf import settings
from django.db.models import Q
import stripe, string, random, qrcode
from namoro.settings import KEY_SECRET_STRIPE, DOMINIO, BASE_DIR
from django.core.files.base import ContentFile
import io
from payment.models import Pedido
from payment.utils import create_confirmation_ticket
from docx.shared import Inches
from django.core.files import File
import requests
from pprint import pprint

def get_perfil_notificacoes(request):
    if request.user.is_authenticated and Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        get_perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

        # Redireciona para profissionais em relacionamento
        """ if get_perfil.interesse == 'Terapias diversas' or get_perfil.interesse == 'Profissionais em relacionamento':
            return redirect('profissionais_relacionamento') """
        
        if Pedido.objects.filter(perfil=get_perfil, plano_ativo=True).exists():
            request.session['meu_pedido'] = True

        request.session['get_perfil_slug'] = get_perfil.slug
        if get_perfil.foto:
            request.session['perfil_foto_url'] = get_perfil.foto.url
        request.session.save()

        todas_notificacoes = []
        __notificacoes = Notificacao.objects.all().order_by('-id')
        for notificacao in __notificacoes:
            if notificacao.convite_evento and notificacao.convite_evento.destinatario == get_perfil:
                todas_notificacoes.append(notificacao)

            elif notificacao.convite_evento and notificacao.convite_evento.remetente == get_perfil:
                todas_notificacoes.append(notificacao)

            elif notificacao.video_chamada and notificacao.video_chamada.destinatario == get_perfil:
                todas_notificacoes.append(notificacao)

            elif notificacao.video_chamada and notificacao.video_chamada.remetente == get_perfil:
                todas_notificacoes.append(notificacao)

        if todas_notificacoes:
            request.session['qtd_notificacoes'] = len(todas_notificacoes)
            request.session.save()
            return todas_notificacoes[:2]
        else:
            request.session['qtd_notificacoes'] = 0
            request.session.save()
    elif request.user.is_staff:
        ...
    else:
        messages.error(request, 'Faça login ou registro para poder ter acesso ao site')
        return 'redirect'


def presenciais(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')
    
    # Filtrando os eventos pelo gênero - Início
    get_perfil_slug = request.session.get('get_perfil_slug', '')
    if Perfil.objects.filter(slug=get_perfil_slug).exists():
        perfil = Perfil.objects.get(slug=get_perfil_slug)
    else:
        perfil = None

    eventos = Evento.objects.filter(tipo='Presencial', visibilidade=True)

    if perfil and perfil.genero == 'Masculino':
        eventos = eventos.exclude(divisao_genero='mulher')
    elif perfil and perfil.genero == 'Feminino':
        eventos = eventos.exclude(divisao_genero='homem')
    # Filtrando os eventos pelo gênero - Fim

    eventos_filtrados = []
    data_atual = datetime.now()
    for evento in eventos:
        if data_atual < evento.data:
            eventos_filtrados.append(evento)

    qtd = len(eventos_filtrados) if eventos_filtrados else 0

    paginator = Paginator(eventos_filtrados, 10)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'presenciais.html', {
        'page_obj': page_obj,
        'qtd': qtd,
        'todas_notificacoes': todas_notificacoes,
    })

    
def online(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')
    
    
    # Filtrando os eventos pelo gênero - Início
    get_perfil_slug = request.session.get('get_perfil_slug', '')
    if Perfil.objects.filter(slug=get_perfil_slug).exists():
        perfil = Perfil.objects.get(slug=get_perfil_slug)
    else:
        perfil = None

    eventos = Evento.objects.filter(tipo='Online', visibilidade=True)

    if perfil and perfil.genero == 'Masculino':
        eventos = eventos.exclude(divisao_genero='mulher')
    elif perfil and perfil.genero == 'Feminino':
        eventos = eventos.exclude(divisao_genero='homem')
    # Filtrando os eventos pelo gênero - Fim

    eventos_filtrados = []
    data_atual = datetime.now()
    for evento in eventos:
        if data_atual < evento.data:
            eventos_filtrados.append(evento)

    qtd = len(eventos_filtrados) if eventos_filtrados else 0

    paginator = Paginator(eventos_filtrados, 10)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'online.html', {
        'page_obj': page_obj,
        'qtd': qtd,
        'todas_notificacoes': todas_notificacoes,
    })


def evento(request, slug):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')
    data_atual = datetime.now()

    amanha = data_atual + timedelta(days=1)
    amanha = amanha.replace(hour=0, minute=0, second=0, microsecond=0)
    data_formatada_amanha = amanha.strftime('%Y-%m-%dT%H:%M')

    if Evento.objects.filter(slug=slug, visibilidade=True).exists():
        evento = Evento.objects.get(slug=slug, visibilidade=True)
        if data_atual < evento.data:
            finalizado = False
        else:
            finalizado = True

        cheio_homem = False
        cheio_mulher = False
        cheio = False
        if evento.divisao_genero != 'metade' and evento.qtd_participantes <= 0:
            cheio = True
        elif evento.divisao_genero != 'metade' and evento.qtd_participantes > 0:
            cheio = False

        elif evento.divisao_genero == 'metade' and evento.qtd_participantes_homens <= 0:
            cheio_homem = True
        elif evento.divisao_genero == 'metade' and evento.qtd_participantes_homens > 0:
            cheio_homem = False

        elif evento.divisao_genero == 'metade' and evento.qtd_participantes_mulheres <= 0:
            cheio_mulher = True
        elif evento.divisao_genero == 'metade' and evento.qtd_participantes_mulheres > 0:
            cheio_mulher = False

        else:
            cheio = False
    else:
        messages.error(request, 'Esse evento não existe ou foi excluido pela administração.')
        return redirect('home')

    if evento and request.user.is_authenticated and Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        _meu_perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
        if ParticipantesEvento.objects.filter(evento=evento, confirmacao='Confirmado', remetente=_meu_perfil).exists():
            participacao_evento = ParticipantesEvento.objects.get(evento=evento, confirmacao='Confirmado', remetente=_meu_perfil)
        else:
            participacao_evento = False
    else:
        participacao_evento = False
        _meu_perfil = False
        
    if evento:
        participantes = ParticipantesEvento.objects.filter(evento=evento, confirmacao='Confirmado')
        qtd = len(participantes) if participantes else 0
        paginator = Paginator(participantes, 10)
        page = request.GET.get('p', 1)
        page_obj = paginator.get_page(page)

        qtd_maxima_criancas = evento.qtd_participantes - 1 if evento.divisao_genero != 'metade' else None
    else:
        qtd_maxima_criancas = None
        page_obj = None

    if request.user.is_authenticated and Pedido.objects.filter(perfil__usuario=request.user, plano_ativo=True, plano__nome='doze_meses').exists():
        meu_pedido_anual = Pedido.objects.get(perfil__usuario=request.user, plano_ativo=True, plano__nome='doze_meses')
    else:
        meu_pedido_anual = None

    if request.method != 'POST':
        return render(request, 'evento.html', {
            'evento': evento,
            'finalizado': finalizado,
            'todas_notificacoes': todas_notificacoes,
            'page_obj': page_obj,
            'data_formatada_amanha': data_formatada_amanha,
            'qtd': qtd,
            'participacao_evento': participacao_evento,
            'cheio': cheio,
            'meu_pedido_anual': meu_pedido_anual,
            'cheio_homem': cheio_homem,
            'cheio_mulher': cheio_mulher,
            'qtd_maxima_criancas': qtd_maxima_criancas,
        })

    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para poder participar de algum evento.')
        return render(request, 'evento.html', {
            'evento': evento,
            'finalizado': finalizado,
            'todas_notificacoes': todas_notificacoes,
            'page_obj': page_obj,
            'data_formatada_amanha': data_formatada_amanha,
            'qtd': qtd,
            'participacao_evento': participacao_evento,
            'cheio': cheio,
            'meu_pedido_anual': meu_pedido_anual,
            'cheio_homem': cheio_homem,
            'cheio_mulher': cheio_mulher,
            'qtd_maxima_criancas': qtd_maxima_criancas,
        })
    
    qtd_criancas = int(request.POST.get('qtd-criancas', 0))

    # Verificação lotação evento - Início
    if evento.divisao_genero != 'metade':
        _qtd_participantes = evento.qtd_participantes
    else:
        if perfil.genero == 'Masculino':
            _qtd_participantes = evento.qtd_participantes_homens
        else:
            _qtd_participantes = evento.qtd_participantes_mulheres

    if _qtd_participantes <= 0:
        messages.error(request, 'Esse evento já esgotou')
        return render(request, 'evento.html', {
            'evento': evento,
            'finalizado': finalizado,
            'todas_notificacoes': todas_notificacoes,
            'page_obj': page_obj,
            'data_formatada_amanha': data_formatada_amanha,
            'qtd': qtd,
            'participacao_evento': participacao_evento,
            'cheio': cheio,
            'meu_pedido_anual': meu_pedido_anual,
            'cheio_homem': cheio_homem,
            'cheio_mulher': cheio_mulher,
            'qtd_maxima_criancas': qtd_maxima_criancas,
        })
    elif evento.presenca_crianca and qtd_criancas and _qtd_participantes - (qtd_criancas + 1) < 0:
        messages.error(request, f'Esse evento só tem {_qtd_participantes} vagas, e você escolheu {qtd_criancas} crianças + você = {qtd_criancas + 1}')
        return render(request, 'evento.html', {
            'evento': evento,
            'finalizado': finalizado,
            'todas_notificacoes': todas_notificacoes,
            'page_obj': page_obj,
            'data_formatada_amanha': data_formatada_amanha,
            'qtd': qtd,
            'participacao_evento': participacao_evento,
            'cheio': cheio,
            'meu_pedido_anual': meu_pedido_anual,
            'cheio_homem': cheio_homem,
            'cheio_mulher': cheio_mulher,
            'qtd_maxima_criancas': qtd_maxima_criancas,
        })
    # Verificação lotação evento - Fim
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        messages.error(request, 'O seu usuário NÃO está atrelado a nenhum perfil. Por favor, fale com o suporte.')
        return render(request, 'evento.html', {
            'evento': evento,
            'finalizado': finalizado,
            'todas_notificacoes': todas_notificacoes,
            'page_obj': page_obj,
            'data_formatada_amanha': data_formatada_amanha,
            'qtd': qtd,
            'participacao_evento': participacao_evento,
            'cheio': cheio,
            'meu_pedido_anual': meu_pedido_anual,
            'cheio_homem': cheio_homem,
            'cheio_mulher': cheio_mulher,
            'qtd_maxima_criancas': qtd_maxima_criancas,
        })
    
    perfil = Perfil.objects.get(usuario=request.user)

    # Verificação da assinatura - Início
    if not Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
        messages.error(request, f'Você não tem nenhuma assinatura ativa. Contrate uma para poder ter acesso a funcionalidade: "Participar de evento".')
        return redirect('planos')
    # Verificação da assinatura - Fim

    if ParticipantesEvento.objects.filter(remetente=perfil, evento=evento, confirmacao='Confirmado').exists():
        messages.error(request, 'Você já está participando desse evento.')
        return render(request, 'evento.html', {
            'evento': evento,
            'finalizado': finalizado,
            'todas_notificacoes': todas_notificacoes,
            'page_obj': page_obj,
            'data_formatada_amanha': data_formatada_amanha,
            'qtd': qtd,
            'participacao_evento': participacao_evento,
            'cheio': cheio,
            'meu_pedido_anual': meu_pedido_anual,
            'cheio_homem': cheio_homem,
            'cheio_mulher': cheio_mulher,
            'qtd_maxima_criancas': qtd_maxima_criancas,
        })
    
    if evento.pagamento == 'Gratuito' or (evento.pagamento == 'Pago' and meu_pedido_anual and meu_pedido_anual.evento_gratis == 'sim' and meu_pedido_anual.qtd_eventos_gratis == 1):
        if ParticipantesEvento.objects.filter(remetente=perfil, evento=evento).exists() and not ParticipantesEvento.objects.filter(remetente=perfil, evento=evento, confirmacao='Confirmado').exists():
            participacao = ParticipantesEvento.objects.get(remetente=perfil, evento=evento)
            participacao.confirmacao = 'Confirmado'
        elif not ParticipantesEvento.objects.filter(remetente=perfil, evento=evento):
            participacao = ParticipantesEvento.objects.create(remetente=perfil, evento=evento, confirmacao='Confirmado')

        if evento.presenca_crianca and qtd_criancas:
            qtd_participantes_gratuito = qtd_criancas + 1
        else:
            qtd_participantes_gratuito = 1

        if evento.qtd_participantes >= qtd_participantes_gratuito:
            if evento.divisao_genero != 'metade':
                evento.qtd_participantes-=qtd_participantes_gratuito
            elif perfil.genero == 'Masculino':
                evento.qtd_participantes_homens-=qtd_participantes_gratuito
            else:
                evento.qtd_participantes_mulheres-=qtd_participantes_gratuito

        # Gerando o QR Code e o Link - Início
        link_confirmacao = f'{DOMINIO}/eventos/aprovar_entrada_evento'

        letras = string.ascii_letters
        digitos = string.digits
        geral = letras + digitos
        while True:
            codigo = ''.join(random.choices(geral, k=40))
            if not ParticipantesEvento.objects.filter(link_confirmacao=f'{link_confirmacao}/{codigo}/').exists():
                break

        file_name = f'qrcode_{codigo}.png'

        imagem_qrcode = qrcode.make(f'{link_confirmacao}/{codigo}/')

        buffer = io.BytesIO()
        imagem_qrcode.save(buffer, format='PNG')
        buffer.seek(0)

        qr_code_file = ContentFile(buffer.read(), name=file_name)
        participacao.codigo = codigo
        participacao.img_qrcode = qr_code_file
        participacao.link_confirmacao = f'{link_confirmacao}/{codigo}/'
        participacao.save()
        # Gerando o QR Code e o Link - Fim

        # Gerando o Bilhete - Início
        if evento.tipo == 'Presencial':
            template_path = BASE_DIR / 'templates' / 'docs' / 'documento_evento_presencial.docx'

            replacements = {
                '{EVENT_NAME}': evento.nome,
                '{PERFIL_NAME}': perfil.nome,
                '{DATA_EVENTO}': evento.data.strftime('%d/%m/%Y %H:%M:%S'),
                '{VALOR_EVENTO}': str(0.0),
                '{LOCALIZACAO}': evento.localizacao if evento.localizacao else '',
                '{QTD_CRIANCAS}': str(qtd_criancas),
            }
        else:
            template_path = BASE_DIR / 'templates' / 'docs' / 'documento_evento_online.docx'

            replacements = {
                '{EVENT_NAME}': evento.nome,
                '{PERFIL_NAME}': perfil.nome,
                '{DATA_EVENTO}': evento.data.strftime('%d/%m/%Y %H:%M:%S'),
                '{VALOR_EVENTO}': str(evento.valor),               
                '{LINK_REUNIAO}': evento.link_reuniao if evento.link_reuniao else '',
                '{QTD_CRIANCAS}': str(qtd_criancas),
            }

        images = {
            '{IMAGE_PLACEHOLDER}': 
            {
                'path': participacao.img_qrcode.path,
                'width': Inches(2),  # Specify width as 2 inches
                'height': Inches(2)  # Specify height as 2 inches
            }
        }
        # pprint(replacements)
        temp_file = create_confirmation_ticket(template_path, replacements, images) # Abra o arquivo temporário como um objeto Django File
        temp_file.seek(0)  # Move o ponteiro do arquivo para o início
        django_file = File(temp_file, name='bilhete_de_confirmacao_final.docx')
        participacao.bilhete.save('bilhete_de_confirmacao_final.docx', django_file) # Salva o arquivo no modelo
        temp_file.close() # Fecha e remove o arquivo temporário
        participacao.save()

        # Gerando o Bilhete - Fim

        # Verificando o evento grátis
        if meu_pedido_anual:
            meu_pedido_anual.evento_gratis = 'nao'
            meu_pedido_anual.qtd_eventos_gratis = 0
            meu_pedido_anual.save()
            messages.success(request, f'Parabéns, você adquiriu esse evento de forma gratuita. Seu saldo de eventos gratuitos: 0')


        if evento.link_reuniao:
            link_reuniao = evento.link_reuniao
        else:
            link_reuniao = 'vazio'

        # Enviando E-mail - Início
        html_content = render_to_string('emails/confirmacao_evento_confirmado.html', 
        {'nome_evento': evento.nome, 
        'descricao': evento.descricao, 
        'nome_perfil': perfil.nome,
        'preco': 'gratuito',
        'link_reuniao': link_reuniao,
        'tipo_evento': evento.tipo,
        'data': evento.data,
        'link': f'{DOMINIO}/perfil/meus_eventos/'})
        text_content = strip_tags(html_content)

        _email = EmailMultiAlternatives(f'Você confirmou o seu convite para o evento "{evento.nome}"', text_content, 
        settings.EMAIL_HOST_USER, [perfil.usuario.email])
        _email.attach_alternative(html_content, 'text/html')
        _email.send()
        # Enviando E-mail - Fim 
        
        convites_eventos = ConviteEvento.objects.filter(destinatario=perfil, evento=evento, confirmacao='Pendente')
        for convite_evento in convites_eventos:
            convite_evento.confirmacao = 'Confirmado'
            convite_evento.save()

            if Notificacao.objects.filter(tipo='Evento', convite_evento=convite_evento, confirmacao='Pendente').exists():
                notificacao = Notificacao.objects.get(tipo='Evento', convite_evento=convite_evento, confirmacao='Pendente')
                notificacao.confirmacao = 'Confirmado'
                notificacao.save()

                # Enviando E-mail - Início
                html_content = render_to_string('emails/convite_evento_confirmado_email.html', 
                {'nome_destinatario': notificacao.convite_evento.destinatario.nome, 
                'nome_remetente': notificacao.convite_evento.remetente.nome,
                'nome_evento': notificacao.convite_evento.evento.nome,
                'data': notificacao.convite_evento.evento.data,
                'tipo_evento': notificacao.convite_evento.evento.tipo,
                'pagamento_evento': notificacao.convite_evento.evento.pagamento,
                'mensagem_evento': notificacao.convite_evento.descricao,
                'link': f'{settings.DOMINIO}/eventos/info/{notificacao.convite_evento.evento.slug}/'})
                text_content = strip_tags(html_content)

                _email = EmailMultiAlternatives(f'"{notificacao.convite_evento.destinatario.nome}" confirmou o seu convite para o evento "{notificacao.convite_evento.evento.nome}"', text_content, 
                settings.EMAIL_HOST_USER, [notificacao.convite_evento.remetente.usuario.email])
                _email.attach_alternative(html_content, 'text/html')
                _email.send()
                # Enviando E-mail - Fim 
        
        participantes = ParticipantesEvento.objects.filter(evento=evento, confirmacao='Confirmado')
        qtd = len(participantes) if participantes else 0
        paginator = Paginator(participantes, 10)
        page = request.GET.get('p', 1)
        page_obj = paginator.get_page(page)

        todas_notificacoes = get_perfil_notificacoes(request)
        if todas_notificacoes == 'redirect':
            return redirect('login')

        messages.success(request, f"""Parabéns, você confirmou a sua presença no evento: "{evento.nome}". 
                      Enviamos um e-mail para você com o qrcode de confirmação. 
                      Guarde ele com muita segurança, pois só poderá entrar no evento com ele.
                      Você também pode ver o qrcode no seu perfil em "Meus eventos".""")
        return redirect(f'{DOMINIO}/eventos/info/{evento.slug}/')


    elif evento.pagamento == 'Pago':

        preco_total_evento = 0
        if evento.divisao_genero == 'homem':
            if perfil.genero != 'Masculino':
                messages.error(request, 'Esse evento é apenas para homens.')
                return render(request, 'evento.html', {
                    'evento': evento,
                    'finalizado': finalizado,
                    'todas_notificacoes': todas_notificacoes,
                    'page_obj': page_obj,
                    'data_formatada_amanha': data_formatada_amanha,
                    'qtd': qtd,
                    'participacao_evento': participacao_evento,
                    'cheio': cheio,
                    'meu_pedido_anual': meu_pedido_anual,
                    'cheio_homem': cheio_homem,
                    'cheio_mulher': cheio_mulher,
                })
            preco_total_evento = evento.valor

        if evento.divisao_genero == 'mulher':
            if perfil.genero != 'Feminino':
                messages.error(request, 'Esse evento é apenas para homens.')
                return render(request, 'evento.html', {
                    'evento': evento,
                    'finalizado': finalizado,
                    'todas_notificacoes': todas_notificacoes,
                    'page_obj': page_obj,
                    'data_formatada_amanha': data_formatada_amanha,
                    'qtd': qtd,
                    'participacao_evento': participacao_evento,
                    'cheio': cheio,
                    'meu_pedido_anual': meu_pedido_anual,
                    'cheio_homem': cheio_homem,
                    'cheio_mulher': cheio_mulher,
                    'qtd_maxima_criancas': qtd_maxima_criancas,
                })
            preco_total_evento = evento.valor

        if evento.divisao_genero == 'metade':
            if perfil.genero != 'Outros':
                messages.error(request, 'Esse evento é apenas para homens e mulheres.')
                return render(request, 'evento.html', {
                    'evento': evento,
                    'finalizado': finalizado,
                    'todas_notificacoes': todas_notificacoes,
                    'page_obj': page_obj,
                    'data_formatada_amanha': data_formatada_amanha,
                    'qtd': qtd,
                    'participacao_evento': participacao_evento,
                    'cheio': cheio,
                    'meu_pedido_anual': meu_pedido_anual,
                    'cheio_homem': cheio_homem,
                    'cheio_mulher': cheio_mulher,
                    'qtd_maxima_criancas': qtd_maxima_criancas,
                })
            elif perfil.genero == 'Masculino':
                preco_total_evento = evento.valor_homem
            else:
                preco_total_evento = evento.valor_mulher

        if evento.divisao_genero == 'nenhum':
            if evento.valor == 0:
                if perfil.genero == 'Masculino':
                    preco_total_evento = evento.valor_homem
                elif perfil.genero == 'Feminino':
                    preco_total_evento = evento.valor_mulher
                else:
                    preco_total_evento = (evento.valor_mulher + evento.valor_homem) / 2
            else:
                preco_total_evento = evento.valor


        if evento.presenca_crianca:
            preco_crianca = qtd_criancas * evento.valor_crianca
            preco_total_evento+=preco_crianca

            format_criancas = f'{qtd_criancas} crianças' if qtd_criancas != 1 else f'{qtd_criancas} criança'
            name_session = f'Evento: {evento.nome}. Pedido: ingresso adulto + {format_criancas} = €{preco_total_evento}'
        else:
            name_session = f'Evento: {evento.nome}.'
        dict_evento = {
            'nome': evento.nome, 
            'preco': preco_total_evento, 
            'slug_evento': evento.slug, 
            'qtd_criancas': qtd_criancas,
            'name_session': name_session,
        }
        request.session['dict_evento'] = dict_evento
        request.session.save()

        if PagamentoEventos.objects.filter(evento=evento, perfil=perfil, pagamento_feito=True).exists():
            messages.error(request, 'Você já está participando desse evento e já pagou por ele.')
            return render(request, 'evento.html', {
                'evento': evento,
                'finalizado': finalizado,
                'todas_notificacoes': todas_notificacoes,
                'page_obj': page_obj,
                'data_formatada_amanha': data_formatada_amanha,
                'qtd': qtd,
                'cheio': cheio,
                'meu_pedido_anual': meu_pedido_anual,
                'cheio_homem': cheio_homem,
                'cheio_mulher': cheio_mulher,
                'qtd_maxima_criancas': qtd_maxima_criancas,
            })
        elif not PagamentoEventos.objects.filter(evento=evento, perfil=perfil).exists():
            pagamento_evento = PagamentoEventos.objects.create(evento=evento, perfil=perfil, preco_pedido=preco_total_evento)
            pagamento_evento.save()
        elif PagamentoEventos.objects.filter(evento=evento, perfil=perfil, status_pedido='pending').exists():
            pagamento_evento = PagamentoEventos.objects.get(evento=evento, perfil=perfil)
            pagamento_evento.preco_pedido = preco_total_evento
            pagamento_evento.save()

        pagamento_evento.qtd_criancas = qtd_criancas
        pagamento_evento.save()

        return redirect(f'{DOMINIO}/payment/create_session/pagamento_evento/{evento.nome}/')
        
    else:
        messages.error(request, 'Tipo de pagamento inválido. Por favor, fale com o suporte.')
        return render(request, 'evento.html', {
            'evento': evento,
            'finalizado': finalizado,
            'todas_notificacoes': todas_notificacoes,
            'page_obj': page_obj,
            'data_formatada_amanha': data_formatada_amanha,
            'qtd': qtd,
            'participacao_evento': participacao_evento,
            'cheio': cheio,
            'meu_pedido_anual': meu_pedido_anual,
            'cheio_homem': cheio_homem,
            'cheio_mulher': cheio_mulher,
            'qtd_maxima_criancas': qtd_maxima_criancas,
        })


def galeria_fotos(request, slug):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not Evento.objects.filter(slug=slug, visibilidade=True).exists():
        return redirect(http_referer)
    
    evento = Evento.objects.get(slug=slug, visibilidade=True)

    return render(request, 'galeria_fotos.html', {
        'evento': evento,
    })
    


def aprovar_entrada_evento(request, codigo):
    if request.user.is_authenticated and request.user.is_staff:
        todas_notificacoes = get_perfil_notificacoes(request)
        if todas_notificacoes == 'redirect':
            return redirect('login')
        validacao = False
        if not ParticipantesEvento.objects.filter(codigo=codigo).exists() or not ParticipantesEvento.objects.filter(codigo=codigo, confirmacao='Confirmado').exists():
            return render(request, 'aprovar_entrada_evento.html', {
                'validacao': validacao,
                'mensagem': 'O qr code enviado NÃO existe e não está atrelado a nenhum usuário.'
            })
        if ParticipantesEvento.objects.filter(codigo=codigo, comparecer_evento='Confirmado', confirmacao='Confirmado').exists():
            return render(request, 'aprovar_entrada_evento.html', {
                'validacao': validacao,
                'mensagem': 'O qr code enviado já foi aprovado por outra pessoa.',
            })
        participacao_evento = ParticipantesEvento.objects.get(codigo=codigo, comparecer_evento='Pendente', confirmacao='Confirmado')
        participacao_evento.comparecer_evento = 'Confirmado'
        participacao_evento.save()
        validacao = True

        return render(request, 'aprovar_entrada_evento.html', {
            'participacao_evento': participacao_evento,
            'validacao': validacao,
            'mensagem': 'O qr code enviado foi aprovado com sucesso. A sua entrada foi liberada',
        })
    else:
        messages.error(request, 'Essa página é só para administradores.')
        return redirect('login')
    
def cadastrar_colaboradores_evento(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method != 'POST':
            return render(request, 'cadastrar_colaboradores_evento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })
        
        username = request.POST.get('username')
        nome = request.POST.get('nome')
        pais = request.POST.get('pais')
        regiao = request.POST.get('regiao')
        email = request.POST.get('email')
        celular = request.POST.get('celular')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')
        recaptcha = request.POST.get('g-recaptcha-response')

        try:
            validate_email(email)
        except:
            messages.error(request, 'E-mail inválido!')
            return render(request, 'cadastrar_colaboradores_evento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })

        # Início - Recaptcha
        if not recaptcha:
            messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
            return render(request, 'cadastrar_colaboradores_evento.html', {
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
            return render(request, 'cadastrar_colaboradores_evento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })
        # Final - Recaptcha

        if len(senha1) < 5:
            messages.error(request, 'As senhas tem que ter no mínimo 5 caracteres!')
            return render(request, 'cadastrar_colaboradores_evento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })

        if senha1 != senha2:
            messages.error(request, 'As senhas devem ser iguais!')
            return render(request, 'cadastrar_colaboradores_evento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'O e-mail enviado já está atrelado a um usuário. Por favor, use outro')
            return render(request, 'cadastrar_colaboradores_evento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'O nome enviado já está atrelado a um usuário. Por favor, use outro')
            return render(request, 'cadastrar_colaboradores_evento.html', {
                'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            })
        
        # Gerando Código - Início
        letras = string.ascii_letters
        digitos = string.digits
        geral = letras + digitos
        while True:
            codigo = ''.join(random.choices(geral, k=25))
            if not ColaboradoresEvento.objects.filter(codigo=codigo, usuario__username=codigo).exists():
                break
        # Gerando Código - Fim
        
        usuario = User.objects.create_user(
            username=username,
            email=email,
            password=senha1,
            is_staff=True,
        )
        usuario.save()
        colaborador = ColaboradoresEvento.objects.create(
            usuario=usuario,
            nome=nome,
            pais=pais,
            celular=celular,
            regiao=regiao,
        )

        colaborador.codigo = codigo
        colaborador.save()

        grupo_colaborador = Group.objects.get(name='colaborador evento')
        usuario.groups.add(grupo_colaborador)

        messages.success(request, f'O colabodador do evento "{colaborador.nome}" foi cadastrado com sucesso')
        return render(request, 'cadastrar_colaboradores_evento.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
        })

    else:
        messages.error(request, 'Essa página é só para administradores.')
        return redirect('login')


def convidar_evento(request, slug_destinatario):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para poder convidar alguém para um evento.')
        return redirect('login')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        messages.error(request, 'O seu usuário NÃO está atrelado a nenhum perfil. Por favor, fale com o suporte.')
        return redirect(http_referer)
    
    perfil = Perfil.objects.get(usuario=request.user)

    # Verificação da assinatura - Início
    if not Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
        messages.error(request, f'Você não tem nenhuma assinatura ativa. Contrate uma para poder ter acesso a funcionalidade: "Convidar para eventos".')
        return redirect('planos')
    # Verificação da assinatura - Fim

    if not Perfil.objects.filter(slug=slug_destinatario).exists():
        messages.error(request, 'O usuário que você está tentando convidar NÃO existe.')
        return redirect(http_referer)
    
    destinatario = Perfil.objects.get(slug=slug_destinatario)

    # Verificação bloqueio - Início
    if BloquearUsuarios.objects.filter(usuario=destinatario, bloqueado=perfil).exists():
        messages.error(request, f'Você não pode convidar "{destinatario.nome}", pois você foi bloqueado.')
        return redirect(http_referer)
    # Verificação bloqueio - Fim
    
    """# Impedindo que perfis com certos interesses sejam chamados para eventos - Início
    if destinatario.interesse == 'Networking e Negocios' or destinatario.interesse == 'Terapias diversas' or destinatario.interesse == 'Profissionais em relacionamento':
        messages.error(request, f'Esse usuário NÃO pode ser convidado para evento, pois o interesse dele é: "{destinatario.interesse}"')
        return redirect(f'{settings.DOMINIO}/perfil/info/{slug_destinatario}/')
    # Impedindo que perfis com certos interesses sejam chamados para eventos - Fim"""

    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    eventos = Evento.objects.filter(visibilidade=True)
    qtd = len(eventos) if eventos else 0

    eventos_filtrados = []
    data_atual = datetime.now()
    for evento in eventos:
        if data_atual < evento.data and evento.qtd_participantes >= 1:
            eventos_filtrados.append(evento)

    paginator = Paginator(eventos_filtrados, 10)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)

    if request.method != 'POST':
        return render(request, 'convidar_evento.html', {
            'page_obj': page_obj,
            'destinatario': destinatario,
            'data_atual': data_atual,
            'qtd': qtd,
            'todas_notificacoes': todas_notificacoes,
        })
    
    slug_evento = request.POST.get('slug_evento')
    descricao = request.POST.get('descricao', '')
    
    if not Evento.objects.filter(slug=slug_evento).exists():
        messages.error(request, 'O evento que você está tentando convidar NÃO existe.')
        return render(request, 'convidar_evento.html', {
            'page_obj': page_obj,
            'destinatario': destinatario,
            'data_atual': data_atual,
            'qtd': qtd,
            'todas_notificacoes': todas_notificacoes,
        })
    
    evento = Evento.objects.get(slug=slug_evento)

    # Se o destinatário já recusou um convite de evento seu, você não pode mais convidar ela para outro evento
    if ConviteEvento.objects.filter(remetente=perfil, destinatario=destinatario, confirmacao='Rejeitado', evento=evento).exists():
        messages.error(request, f'Você NÃO pode mais convidar "{destinatario.nome}" para um evento, pois ele(a) já rejeitou um convite seu de evento.')
        return redirect(http_referer)

    # Verificação lotação evento - Início
    if evento.qtd_participantes <= 0:
        messages.error(request, 'Esse evento já esgotou')
        return render(request, 'convidar_evento.html', {
            'page_obj': page_obj,
            'destinatario': destinatario,
            'data_atual': data_atual,
            'qtd': qtd,
            'todas_notificacoes': todas_notificacoes,
        })
    # Verificação lotação evento - Fim
    
    if ConviteEvento.objects.filter(evento=evento, remetente=perfil, destinatario=destinatario).exists():
        messages.error(request, f'Você já convidou "{destinatario.nome}" para o evento "{evento.nome}"')
        return render(request, 'convidar_evento.html', {
            'page_obj': page_obj,
            'destinatario': destinatario,
            'data_atual': data_atual,
            'qtd': qtd,
            'todas_notificacoes': todas_notificacoes,
        })
    
    if descricao and len(descricao) > 2000:
        messages.error(request, f'A descrição não pode ter mais que 2000 caracteres.')
        return render(request, 'convidar_evento.html', {
            'page_obj': page_obj,
            'destinatario': destinatario,
            'data_atual': data_atual,
            'qtd': qtd,
            'todas_notificacoes': todas_notificacoes,
        })

    convite_evento = ConviteEvento.objects.create(evento=evento, remetente=perfil, destinatario=destinatario, descricao=descricao)
    convite_evento.save()

    if not Notificacao.objects.filter(tipo='Evento', convite_evento=convite_evento).exists():
        notificacao_evento = Notificacao.objects.create(tipo='Evento', convite_evento=convite_evento)
        notificacao_evento.save()

    # Enviando E-mail - Início
    html_content = render_to_string('emails/convite_evento_email.html', 
    {'nome_destinatario': notificacao_evento.convite_evento.destinatario.nome, 
    'nome_remetente': notificacao_evento.convite_evento.remetente.nome,
    'nome_evento': notificacao_evento.convite_evento.evento.nome,
    'data': notificacao_evento.convite_evento.evento.data,
    'tipo_evento': notificacao_evento.convite_evento.evento.tipo,
    'pagamento_evento': notificacao_evento.convite_evento.evento.pagamento,
    'mensagem_evento': notificacao_evento.convite_evento.descricao,
    'link': f'{settings.DOMINIO}/eventos/info/{notificacao_evento.convite_evento.evento.slug}/'})
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives(f'Você foi convidado para um evento - FINDB', text_content, 
    settings.EMAIL_HOST_USER, [notificacao_evento.convite_evento.destinatario.usuario.email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim

    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')
    
    messages.success(request, f'Parabéns. Você convidou "{destinatario.nome}" para o evento "{evento.nome}". Aguarde a confirmação dela.')
    return render(request, 'convidar_evento.html', {
        'page_obj': page_obj,
        'destinatario': destinatario,
        'data_atual': data_atual,
        'qtd': qtd,
        'todas_notificacoes': todas_notificacoes,
    })


def notificacoes(request, slug):
    if not request.user.is_authenticated:
        messages.error(request, 'Faça login para poder convidar alguém para um evento.')
        return redirect('login')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        messages.error(request, 'O seu usuário NÃO está atrelado a nenhum perfil. Por favor, fale com o suporte.')
        return redirect('logout')
    
    perfil = Perfil.objects.get(usuario=request.user)
    
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    _notificacoes = Notificacao.objects.all().order_by('-id')
    minhas_notificacoes = []

    for _notificacao in _notificacoes:
        if _notificacao.convite_evento and _notificacao.convite_evento.destinatario == perfil:
            minhas_notificacoes.append(_notificacao)
        elif _notificacao.convite_evento and _notificacao.convite_evento.remetente == perfil:
            minhas_notificacoes.append(_notificacao)

        elif _notificacao.video_chamada and _notificacao.video_chamada.destinatario == perfil:
            minhas_notificacoes.append(_notificacao)
        elif _notificacao.video_chamada and _notificacao.video_chamada.remetente == perfil:
            minhas_notificacoes.append(_notificacao)

    paginator = Paginator(minhas_notificacoes, 10)
    page = request.GET.get('p', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'notificacoes.html', {
        'page_obj': page_obj,
        'todas_notificacoes': todas_notificacoes,
    })


def rejeitar_notificacao(request, id):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not request.user.is_authenticated:
        return redirect('home')

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return redirect('home')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not Notificacao.objects.filter(id=id).exists() or not Notificacao.objects.filter(id=id, confirmacao='Pendente').exists():
        return redirect('home')
    
    notificacao = Notificacao.objects.get(id=id)
    notificacao.confirmacao = 'Rejeitado'
    notificacao.save()

    for _notificacao in Notificacao.objects.all():
        if _notificacao.convite_evento and _notificacao.convite_evento.destinatario == perfil:
            _notificacao.convite_evento.confirmacao = 'Rejeitado'
            _notificacao.convite_evento.save()
            messages.success(request, 'Você rejeitou o convite')

            # Enviando E-mail - Início
            html_content = render_to_string('emails/convite_evento_rejeitado_email.html', 
            {'nome_destinatario': _notificacao.convite_evento.destinatario.nome, 
            'nome_remetente': _notificacao.convite_evento.remetente.nome,
            'nome_evento': _notificacao.convite_evento.evento.nome,
            'link': f'{settings.DOMINIO}/perfil/filtro/pessoas/'})
            text_content = strip_tags(html_content)

            _email = EmailMultiAlternatives(f'"{_notificacao.convite_evento.destinatario.nome}" rejeitou o seu convite para o evento "{_notificacao.convite_evento.evento.nome}"', text_content, 
            settings.EMAIL_HOST_USER, [_notificacao.convite_evento.remetente.usuario.email])
            _email.attach_alternative(html_content, 'text/html')
            _email.send()
            # Enviando E-mail - Fim

            break
        elif _notificacao.video_chamada and _notificacao.video_chamada.destinatario == perfil:
            _notificacao.video_chamada.confirmacao = 'Rejeitado'
            _notificacao.video_chamada.save()

            # Enviando E-mail - Início
            html_content = render_to_string('emails/convite_chamada_video_rejeitado.html', 
            {'nome_destinatario': _notificacao.video_chamada.destinatario.nome, 
            'nome_remetente': _notificacao.video_chamada.remetente.nome,
            'link': f'{settings.DOMINIO}/perfil/filtro/pessoas/'})
            text_content = strip_tags(html_content)

            _email = EmailMultiAlternatives(f'"{_notificacao.video_chamada.destinatario.nome}" rejeitou o seu convite para chamada de vídeo', text_content, 
            settings.EMAIL_HOST_USER, [_notificacao.video_chamada.remetente.usuario.email])
            _email.attach_alternative(html_content, 'text/html')
            _email.send()
            # Enviando E-mail - Fim
            break

    return redirect(f'{settings.DOMINIO}/eventos/notificacoes/{perfil.slug}/')


def apagar_notificacao(request, id):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not request.user.is_authenticated:
        return redirect('home')

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return redirect('home')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not Notificacao.objects.filter(id=id).exists() or Notificacao.objects.filter(id=id, confirmacao='Pendente').exists():
        return redirect(http_referer)
    
    notificacao = Notificacao.objects.get(id=id)
    notificacao.delete()

    messages.success(request, 'A notificação foi apagada com sucesso.')
    return redirect(f'{settings.DOMINIO}/eventos/notificacoes/{perfil.slug}/')