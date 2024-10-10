from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
import stripe
from namoro.settings import KEY_PUBLIC_STRIPE, KEY_SECRET_STRIPE, KEY_WEBHOOK, DOMINIO, BASE_DIR
from django.views.decorators.csrf import csrf_exempt
from .models import Plano, Pedido, PagamentoEventos
from eventos.models import Evento, ParticipantesEvento, ConviteEvento, Notificacao
from eventos.views import get_perfil_notificacoes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string	
from django.utils.html import strip_tags			
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from perfil.models import Perfil
from django.contrib.auth.models import User
from django.contrib import auth
import requests
from django.db.models import Q
import string, random, qrcode
from django.core.files.base import ContentFile
import io
from payment.utils import create_confirmation_ticket
from docx.shared import Inches
from django.core.files import File

def planos(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    if request.user.is_authenticated and Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
        if Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
            nome_plano = Pedido.objects.get(perfil=perfil, plano_ativo=True).plano.nome
        else:
            nome_plano = ''
    else:
        nome_plano = ''

    return render(request, 'planos.html', {
        'todas_notificacoes': todas_notificacoes,
        'nome_plano': nome_plano,
    })

def success(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    return render(request, 'success.html', {
        'todas_notificacoes': todas_notificacoes,
    })

def reject(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    return render(request, 'reject.html', {
        'todas_notificacoes': todas_notificacoes,
    })

def payment_event_success(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    return render(request, 'payment_event_success.html', {
        'todas_notificacoes': todas_notificacoes,
    })

def upgrade_success(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    return render(request, 'upgrade_success.html', {
        'todas_notificacoes': todas_notificacoes,
    })


def upgrade_plan(request, plano):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar online. Se não tiver uma ainda, crie uma conta.')
        return redirect('login')
    
    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        messages.error(request, 'Seu usuário não está atrelado a um perfil. Por favor, fale com o suporte.')
        return redirect('login')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
    if not Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
        messages.error(request, 'Você não pode trocar de plano, pois não tem um plano ativo. Contrate um plano')
        return redirect('planos')
    
    pedido = Pedido.objects.get(perfil=perfil, plano_ativo=True)

    if pedido.plano.nome == plano:
        messages.error(request, 'Você já tem esse plano. Troque por outro.')
        return redirect('planos')
    elif pedido.plano.nome == 'doze_meses' and plano == 'doze_meses':
        messages.error(request, 'Você não pode trocar o seu plano para um inferior, apenas para um superior.')
        return redirect('planos')
    elif pedido.plano.nome == 'seis_meses' and plano == 'tres_meses':
        messages.error(request, 'Você não pode trocar o seu plano para um inferior, apenas para um superior.')
        return redirect('planos')
    elif pedido.plano.nome == 'doze_meses' and plano == 'seis_meses':
        messages.error(request, 'Você não pode trocar o seu plano para um inferior, apenas para um superior.')
        return redirect('planos')
    elif pedido.plano.nome == 'doze_meses' and plano == 'tres_meses':
        messages.error(request, 'Você não pode trocar o seu plano para um inferior, apenas para um superior.')
        return redirect('planos')
    
    if plano == 'tres_meses':
        plano_obj = Plano.objects.filter(nome='tres_meses').first()
        codigo = plano_obj.codigo
    elif plano == 'seis_meses':
        plano_obj = Plano.objects.filter(nome='seis_meses').first()
        codigo = plano_obj.codigo
    elif plano == 'doze_meses':
        plano_obj = Plano.objects.filter(nome='doze_meses').first()
        codigo = plano_obj.codigo
    else:
        messages.error(request, f'O plano enviado: "{plano}" é inválido. Por favor, fale com o suporte.')
        return redirect('planos')
    
    stripe.api_key = KEY_SECRET_STRIPE
    # Recuperando a assinatura atual para encontrar o ID do item de assinatura
    subscription = stripe.Subscription.retrieve(pedido.id_assinatura)
    # Mudando o primeiro item da assinatura
    subscription_item_id = subscription["items"]["data"][0]["id"]
    # Atualizando a assinatura, mandando o id da produto/assinatura/subscription
    stripe.Subscription.modify(
        pedido.id_assinatura,
        items=[{"id": subscription_item_id, "price": codigo, "quantity": 1}],
        metadata={
            'perfil_slug': perfil.slug,
            'plano_codigo': codigo,
            'upgrade': True,
        },
    )

    return redirect('upgrade_success')


# Cancelar Perfil Definitivamente - Início
def perfil_cancelamento_assinatura(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar online. Se não tiver uma ainda, crie uma conta.')
        return redirect('login')
    
    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        messages.error(request, 'Seu usuário não está atrelado a um perfil. Por favor, fale com o suporte.')
        return redirect('login')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
    if Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
        messages.error(request, 'Você não pode excluir o seu perfil, pois tem um plano ativo. Antes de excluir, você tem que cancelar o plano ativo que você tem.')
        messages.info(request, 'Acesse o link no final da página para acessar o gerenciamento da sua assinatura.')
        return redirect('meu_perfil')

    # Gerando Código - Início
    letras = string.ascii_letters
    digitos = string.digits
    # caracteres = '!@#$%&*._-'

    geral = letras + digitos
    while True:
        codigo = ''.join(random.choices(geral, k=30))
        if not Perfil.objects.filter(codigo_cancelar_assinatura=codigo).exists():
            break
    # Gerando Código - Fim
    perfil.codigo_cancelar_assinatura = codigo
    perfil.save()

    # Enviando E-mail - Início
    html_content = render_to_string('emails/pedido_cancelamento_perfil_email.html', 
    {
    'nome': perfil.nome,
    'link': f'{settings.DOMINIO}/payment/excluir_perfil/{codigo}/'
    })
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('Você solicitou a exclusão definitiva da sua conta - FINDB', text_content, 
    settings.EMAIL_HOST_USER, [perfil.usuario.email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim

    return render(request, 'perfil_cancelamento_assinatura.html')


def excluir_perfil(request, codigo):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar online para realizar essa operação.')
        return redirect('login')
    
    if not Perfil.objects.filter(codigo_cancelar_assinatura=codigo).exists():
        return redirect('home')
    
    perfil = Perfil.objects.get(codigo_cancelar_assinatura=codigo)
    
    if request.method != 'POST':
        return render(request, 'excluir_perfil.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'codigo': codigo,
        })
    
    email = request.POST.get('email')
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')
    recaptcha = request.POST.get('g-recaptcha-response')

    # Início - Recaptcha
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'excluir_perfil.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
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
        return render(request, 'excluir_perfil.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'codigo': codigo,
        })
    # Final - Recaptcha

    if senha1 != senha2:
        messages.error(request, 'As senhas precisam ser iguais.')
        return render(request, 'excluir_perfil.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'codigo': codigo,
        })

    if not User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail enviado NÃO está atrelado a nenhuma conta.')
        return render(request, 'excluir_perfil.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'codigo': codigo,
        })
    
    usuario = User.objects.get(email=email)

    if perfil.usuario != usuario:
        messages.error(request, 'Coloque o e-mail da sua conta.')
        return render(request, 'excluir_perfil.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'codigo': codigo,
        })

    user = auth.authenticate(request, username=usuario.username, password=senha1)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'excluir_perfil.html', {
            'RECAPTCHA_FRONT': settings.RECAPTCHA_FRONT,
            'codigo': codigo,
        })

    # Enviando E-mail - Início
    html_content = render_to_string('emails/perfil_excluido_email.html', 
    {
    'nome': perfil.nome,
    'link': f'{settings.DOMINIO}/'
    })
    text_content = strip_tags(html_content)

    _email = EmailMultiAlternatives('O seu perfil foi excluido - FINDB', text_content, 
    settings.EMAIL_HOST_USER, [perfil.usuario.email])
    _email.attach_alternative(html_content, 'text/html')
    _email.send()
    # Enviando E-mail - Fim

    perfil.usuario.delete()

    return render(request, 'perfil_excluido.html')


def perfil_excluido(request):
    todas_notificacoes = get_perfil_notificacoes(request)
    if todas_notificacoes == 'redirect':
        return redirect('login')

    return render(request, 'perfil_excluido.html', {
        'todas_notificacoes': todas_notificacoes,
    })
# Cancelar Perfil Definitivamente - Fim


# Trocar dados de cartão, cancelar assinatura e ver histórico de pagamentos - Início
""" def gerenciamento_assinatura(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar online. Se não tiver uma ainda, crie uma conta.')
        return redirect('login')
    
    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        messages.error(request, 'Seu usuário não está atrelado a um perfil. Por favor, fale com o suporte.')
        return redirect('login')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
    if not Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
        messages.error(request, 'Você não pode gerenciar a sua assinatura, pois não tem um plano ativo. Contrate um plano')
        return redirect('meu_perfil')
    
    pedido = Pedido.objects.get(perfil=perfil, plano_ativo=True)

    if pedido.status_pedido != 'approved' and pedido.status_pedido != 'paused':
        messages.error(request, 'Você não pode gerenciar a sua assinatura, pois não tem um plano ativo. Contrate um plano')
        return redirect('meu_perfil')

    # Mandando o id da assinatura e cancelando ela
    # Tem que customizar o portal, em: https://dashboard.stripe.com/test/settings/billing/portal
    # Escolha as configurações que você deseja, salve as alterações e gere o link
    stripe.api_key = KEY_SECRET_STRIPE
    response = stripe.billing_portal.Session.create(
        customer=pedido.id_user,
        return_url=f'{settings.DOMINIO}/perfil/meu_perfil/',
    )

    url = response.get('url')
    if url:
        return redirect(url)
    else:
        messages.error(request, 'Ocorreu algum erro com a parte gerenciamento da assinatura. Por favor, fale com o suporte!')
        return redirect('home') """

# Trocar dados de cartão, cancelar assinatura e ver histórico de pagamentos - Fim

# Gerenciamento de assinaturas e pagamentos individuais com STRIPE
# Criando uma sessão de pagamentos, podendo ser assinatura, ou pagamento único
def create_session(request, tipo_pagamento, info):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not request.user.is_authenticated:
        messages.error(request, 'Para realizar o pagamento, você precisa estar online. Se não tiver uma ainda, crie uma conta.')
        return redirect('login')
    
    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        messages.error(request, 'Seu usuário não está atrelado a um perfil. Por favor, fale com o suporte.')
        return redirect('login')
    
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)
    
    stripe.api_key = KEY_SECRET_STRIPE

    if tipo_pagamento == 'assinatura':

        # Impedindo quem já tem um assinatura ativa, prossiga
        if Pedido.objects.filter(perfil=perfil, plano_ativo=True).exists():
            messages.error(request, 'Você já tem um plano ativo. Caso deseje trocar de plano, aperte no botão de fazer upgrade do plano correspondente.')
            return redirect('planos')
        
        # Todos os planos tem que existir para prosseguir
        if not Plano.objects.filter(nome='tres_meses').exists() and not Plano.objects.filter(nome='seis_meses').exists() and not Plano.objects.filter(nome='doze_meses').exists():
            messages.error(request, f'Nem todos os planos foram cadastrados ainda. Fale com o suporte.')
            return redirect('planos')

        # Na sua dashboard, criar em catalogo de produtos as assinaturas com pagamento recorrente
        # Pegar o código do produto e colocar aqui
        if info == 'tres_meses':
            plano = Plano.objects.filter(nome='tres_meses').first()
            codigo = plano.codigo
        elif info == 'seis_meses':
            plano = Plano.objects.filter(nome='seis_meses').first()
            codigo = plano.codigo
        elif info == 'doze_meses':
            plano = Plano.objects.filter(nome='doze_meses').first()
            codigo = plano.codigo
        else:
            messages.error(request, f'O plano enviado: "{info}" é inválido. Por favor, fale com o suporte.')
            return redirect('planos')

        # Irá criar e redirecionar o usuário para uma sessão de pagamentos
        response = stripe.checkout.Session.create(
            success_url=f'{DOMINIO}/payment/success/',
            cancel_url=f'{DOMINIO}/payment/reject/',
            line_items=[{"price": codigo, "quantity": 1}],
            mode="subscription", # Informa que é uma assinatura
            # O metadata vai ser enviado no último evento: checkout.session.completed 
            #metadata={
                #'perfil_slug': perfil.slug,
                #'plano_codigo': plano.codigo,
            #},
            # Metadata relacionado com a assinatura/subscription
            subscription_data={
                'metadata': {
                    'perfil_slug': perfil.slug,
                    'plano_codigo': codigo,
                }
            },
        )

        # Criando o pedido
        if not Pedido.objects.filter(perfil=perfil).exists():
            pedido = Pedido.objects.create(perfil=perfil, plano=plano, preco_pedido=plano.preco)
            pedido.save()
        else:
            pedido = Pedido.objects.get(perfil=perfil)
            if pedido.status_pedido == 'pending' or pedido.status_pedido == 'rejected' or pedido.status_pedido == 'cancel':
                pedido.plano = plano
                pedido.preco_pedido = plano.preco
                pedido.save()
            else:
                messages.error(request, f'Se a sua assinatura estiver aprovado ou pausado, você não pode contratar outra assinatura, pois você já tem uma ativa')
                messages.info(request, f"""Se a sua assinatura estiver pausado, 
                               quer dizer que tentamos realizar o pagamento no seu 
                               cartão, mas não conseguimos, provavelmente por falta de limite, ou erro no cartão. 
                               Se o problema for limite, vamos esperar uns dias para ver se o cartão liberou limite. 
                               Se não conseguirmos realizar o pagamento novamente, sua assinatura será cancelada. 
                               Para resolver o problema mais facilmente, troque o cartão de crédito como método de pagamento
                               na área do seu perfil.""")
                return redirect('planos')
            
        # Configurando o evento grátis
        if pedido.plano.nome == 'doze_meses':
            pedido.evento_gratis = 'sim'
            pedido.qtd_eventos_gratis = 1
            pedido.save()

    elif tipo_pagamento == 'pagamento_evento':

        if not request.session.get('dict_evento'):
            messages.error(request, f'Ocorreu um erro e os valores do evento estão vazios. Por favor, fale com o suporte')
            return redirect(http_referer)    

        dict_evento = request.session.get('dict_evento')

        # Impedindo quem já pagou pelo evento, prossiga
        if PagamentoEventos.objects.filter(evento__slug=dict_evento.get('slug_evento'), perfil=perfil, pagamento_feito=True).exists():
            messages.error(request, 'Você já está participando desse evento e já pagou por ele.')
            return redirect('planos')

        dict_evento_nome = dict_evento.get('nome')
        dict_name_session = dict_evento.get('name_session', f'Evento: {dict_evento_nome}')    
        
        # Irá criar e redirecionar o usuário para uma sessão de pagamentos
        response = stripe.checkout.Session.create(
            success_url=f'{DOMINIO}/payment/payment_event_success/',
            cancel_url=f'{DOMINIO}/payment/reject/',
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': dict_name_session,
                        },
                        'unit_amount': int(dict_evento.get('preco') * 100),
                    },
                    'quantity': 1,
                }
            ],
            metadata={
                'slug_evento': dict_evento.get('slug_evento'),
                'perfil_slug': perfil.slug,
                'pagamento_evento': True,
            },
        )
        
    else:
        messages.error(request, f'O tipo de pagamento enviado: "{tipo_pagamento}" é inválido. Por favor, fale com o suporte')


    url = response.get('url')
    if url:
        return redirect(url)
    else:
        messages.error(request, 'Ocorreu algum erro com a parte de pagamento. Por favor, fale com o suporte!')
        return redirect('home')


@csrf_exempt
def webhook(request):
    try:
        # payload = json.loads(request.body)
        payload = request.body.decode('utf-8')
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    except:
        return HttpResponse(status=401)

    try:
        # Verifica se o payload é válido e se veio da stripe mesmo
        event = stripe.Webhook.construct_event(
            payload, sig_header, KEY_WEBHOOK
        )
    except ValueError as e:
        return HttpResponse(status=402)

    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=403)

    try:
        event_type = event['type']
    except:
        return HttpResponse(status=404)

    # Quando o cliente atualiza os dados do cartão OU quando o preço da assinatura é altera OU quando a assinatura é feita pela 1 vez
    if event_type == "customer.subscription.updated":
        try:
            status = event.get('data').get('object').get('status')
        except:
            return HttpResponse(status=405)

        if status == "active":
            try:
                subscription = event['data']['object']
                codigo_plano = subscription['items']['data'][0]['plan']['id']
                codigo_cliente = subscription['customer']
                id_assinatura = subscription['id']
                current_period_end = subscription['current_period_end']

                # Pegando os dados do metadata - Dados necessários que eu mando pro webhook na criação da sessão
                perfil_slug = subscription['metadata']['perfil_slug']
                plano_codigo = subscription['metadata']['plano_codigo']
                if subscription.get('metadata') and subscription.get('metadata').get('upgrade'):
                    upgrade = subscription['metadata']['upgrade']
                else:
                    upgrade = False

                """ with open('E:\\Projetos Visual Code\\Python_Freelancer\\FINDB\\payment\\log.txt', 'a+', encoding='utf-8') as file:
                    file.write(f'{codigo_cliente} \n')
                    file.write(f'{id_assinatura} \n')
                    file.write(f'{codigo_plano} \n')
                    file.write(f'{current_period_end} \n')
                    file.write(f'{upgrade} \n') """
            except:
                return HttpResponse(status=406)
            
            if not Perfil.objects.filter(slug=perfil_slug).exists():
                return HttpResponse(status=407)
            
            perfil = Perfil.objects.get(slug=perfil_slug)

            if not Plano.objects.filter(codigo=plano_codigo).exists():
                return HttpResponse(status=408)
            plano = Plano.objects.get(codigo=plano_codigo)
            
            if not upgrade:
                if not Pedido.objects.filter(perfil=perfil):
                    pedido = Pedido.objects.create(
                        perfil=perfil, 
                        plano=plano, 
                        preco_pedido=plano.preco,
                        id_user=codigo_cliente, # Mais importante - id do usuário
                        id_assinatura=id_assinatura, # Mais importante - id da assinatura
                        current_period_end=current_period_end,
                        plano_ativo=True,
                        status_pedido='approved',
                    )
                    pedido.save()
                else:
                    pedido = Pedido.objects.get(perfil=perfil)
                    pedido.id_user = codigo_cliente
                    pedido.id_assinatura = id_assinatura
                    pedido.current_period_end = current_period_end
                    pedido.plano_ativo = True
                    pedido.status_pedido = 'approved'
                    pedido.save()
                
                if not pedido.recebeu_email_aprovado:
                    # Enviando E-mail - Início
                    html_content = render_to_string('emails/assinatura_confirmada_email.html', 
                    {
                    'nome': perfil.nome,
                    'plano_nome': plano.nome.replace('_', ' ').title(), 
                    'preco_pedido': pedido.preco_pedido, 
                    'data_pedido': pedido.data_pedido, 
                    'link': f'{settings.DOMINIO}/perfil/filtro/pessoas/'
                    })
                    text_content = strip_tags(html_content)

                    _email = EmailMultiAlternatives('Assinatura Confirmada - FINDB', text_content, 
                    settings.EMAIL_HOST_USER, [perfil.usuario.email])
                    _email.attach_alternative(html_content, 'text/html')
                    _email.send()
                    # Enviando E-mail - Fim

                    pedido.recebeu_email_aprovado = True
                    pedido.save()

            else:
                if Pedido.objects.filter(perfil=perfil, plano_ativo=True):
                    pedido = Pedido.objects.get(perfil=perfil)
                    if pedido.id_user == codigo_cliente and pedido.id_assinatura == id_assinatura:
                        pedido.current_period_end = current_period_end
                        pedido.plano = plano
                        pedido.preco_pedido = plano.preco
                        pedido.plano_ativo = True
                        pedido.status_pedido = 'approved'

                        # Configurando o evento grátis
                        if pedido.plano.nome != 'doze_meses':
                            pedido.evento_gratis = 'nao'
                            pedido.qtd_eventos_gratis = 0
                        else:
                            pedido.evento_gratis = 'sim'
                            pedido.qtd_eventos_gratis = 1

                        pedido.save()

                        # Enviando E-mail - Início
                        html_content = render_to_string('emails/assinatura_atualizada_email.html', 
                        {
                        'nome': perfil.nome,
                        'plano_nome': plano.nome.replace('_', ' ').title(), 
                        'preco_pedido': pedido.preco_pedido, 
                        'data_atualizacao': pedido.data_ultima_atualizacao, 
                        'link': f'{settings.DOMINIO}/perfil/filtro/pessoas/'
                        })
                        text_content = strip_tags(html_content)

                        _email = EmailMultiAlternatives('Assinatura Atualizada - FINDB', text_content, 
                        settings.EMAIL_HOST_USER, [perfil.usuario.email])
                        _email.attach_alternative(html_content, 'text/html')
                        _email.send()
                        # Enviando E-mail - Fim
                else:
                    return HttpResponse(status=409)
            
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=410)
    
    # Quando o cartão do cliente não tem limite e o pagamento não é feito
    elif event_type == "customer.subscription.paused":
        try:
            subscription = event['data']['object']
            codigo_cliente = subscription['customer']
            id_assinatura = subscription['id']
        except:
            return HttpResponse(status=412)

        if Pedido.objects.filter(id_user=codigo_cliente, id_assinatura=id_assinatura).exists():
            pedido = Pedido.objects.get(id_user=codigo_cliente, id_assinatura=id_assinatura)
            pedido.plano_ativo = False
            pedido.status_pedido = 'paused'
            pedido.save()

            # Enviando E-mail - Início
            html_content = render_to_string('emails/assinatura_pausada_email.html', 
            {
            'nome': pedido.perfil.nome,
            'plano_nome': pedido.plano.nome.replace('_', ' ').title(), 
            'preco_pedido': pedido.pedido.preco_pedido, 
            'data_pagamento': pedido.data_ultima_atualizacao, 
            'link': f'{settings.DOMINIO}/perfil/meu_perfil/'
            })
            text_content = strip_tags(html_content)

            _email = EmailMultiAlternatives('Assinatura Pausada - FINDB', text_content, 
            settings.EMAIL_HOST_USER, [pedido.perfil.usuario.email])
            _email.attach_alternative(html_content, 'text/html')
            _email.send()
            # Enviando E-mail - Fim

        return HttpResponse(status=200)

    # Quando pagamento é feito depois de um paused
    elif event_type == "customer.subscription.resumed":
        try:
            subscription = event['data']['object']
            codigo_cliente = subscription['customer']
            id_assinatura = subscription['id']
        except:
            return HttpResponse(status=414)

        if Pedido.objects.filter(id_user=codigo_cliente, id_assinatura=id_assinatura).exists():
            pedido = Pedido.objects.get(id_user=codigo_cliente, id_assinatura=id_assinatura)
            pedido.plano_ativo = True
            pedido.status_pedido = 'approved'
            pedido.save()

            # Enviando E-mail - Início
            html_content = render_to_string('emails/assinatura_retomada_email.html', 
            {
            'nome': pedido.perfil.nome,
            'plano_nome': pedido.plano.nome.replace('_', ' ').title(), 
            'preco_pedido': pedido.pedido.preco_pedido, 
            'data_pagamento': pedido.data_ultima_atualizacao, 
            'link': f'{settings.DOMINIO}/perfil/filtro/pessoas/'
            })
            text_content = strip_tags(html_content)

            _email = EmailMultiAlternatives('Assinatura Ativa - Pagamento efetuado com sucesso - FINDB', text_content, 
            settings.EMAIL_HOST_USER, [pedido.perfil.usuario.email])
            _email.attach_alternative(html_content, 'text/html')
            _email.send()
            # Enviando E-mail - Fim

        return HttpResponse(status=200)

    # Cliente cancela a assinatura OU a stripe cancela por falta de limite depois de um tempo
    elif event_type == "customer.subscription.deleted":
        try:
            subscription = event['data']['object']
            codigo_cliente = subscription['customer']
            id_assinatura = subscription['id']
        except:
            return HttpResponse(status=414)

        if Pedido.objects.filter(id_user=codigo_cliente, id_assinatura=id_assinatura).exists():
            pedido = Pedido.objects.get(id_user=codigo_cliente, id_assinatura=id_assinatura)
            pedido.plano_ativo = False
            pedido.recebeu_email_aprovado = False
            pedido.status_pedido = 'cancel'
            pedido.save()

            # Enviando E-mail - Início
            html_content = render_to_string('emails/assinatura_cancelada_email.html', 
            {
            'nome': pedido.perfil.nome,
            'link': f'{settings.DOMINIO}/'
            })
            text_content = strip_tags(html_content)

            _email = EmailMultiAlternatives('A sua assinatura foi cancelada - FINDB', text_content, 
            settings.EMAIL_HOST_USER, [pedido.perfil.usuario.email])
            _email.attach_alternative(html_content, 'text/html')
            _email.send()
            # Enviando E-mail - Fim
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=415)
    
    # Esse webhook tem em todas as transações, assinaturas ou não
    # Mas irei tratar apenas os pagamentos únicos, sem ser assinatura
    elif event_type == "checkout.session.completed":

        """with open('E:\\Projetos Visual Code\\Python_Freelancer\\FINDB\\payment\\log.txt', 'a+', encoding='utf-8') as file:
            file.write(f'{event} \n')"""
        try:
            status = event.get('data').get('object').get('payment_status')
            payment_intent = event.get('data').get('object').get('payment_intent')
            pagamento_evento = event.get('data').get('object').get('metadata').get('pagamento_evento')
            perfil_slug = event.get('data').get('object').get('metadata').get('perfil_slug')
            slug_evento = event.get('data').get('object').get('metadata').get('slug_evento')
        except:
            return HttpResponse(status=412)
        
        if not Evento.objects.filter(slug=slug_evento).exists():
            return HttpResponse(status=413)
        
        if not Perfil.objects.filter(slug=perfil_slug).exists():
            return HttpResponse(status=414)
        
        perfil = Perfil.objects.get(slug=perfil_slug)
        evento = Evento.objects.get(slug=slug_evento)

        if ParticipantesEvento.objects.filter(remetente=perfil, evento=evento, confirmacao='Confirmado').exists():
            return HttpResponse(status=415)
        
        if status == 'paid' and pagamento_evento:
    
            if not PagamentoEventos.objects.filter(evento=evento, perfil=perfil).exists():
                pagamento_evento = PagamentoEventos.objects.create(evento=evento, perfil=perfil)
            else:
                pagamento_evento = PagamentoEventos.objects.get(evento=evento, perfil=perfil)

            # Verificando se o evento já esgotou - Início
            if evento.divisao_genero != 'metade':
                qtd_participantes = evento.qtd_participantes
            else:
                if perfil.genero == 'Masculino':
                    qtd_participantes = evento.qtd_participantes_homens
                else:
                    qtd_participantes = evento.qtd_participantes_mulheres

            qtd_participantes_pago = pagamento_evento.qtd_criancas + 1

            if qtd_participantes <= 0 or (evento.presenca_crianca and qtd_participantes - qtd_participantes_pago < 0):
                stripe.api_key = KEY_SECRET_STRIPE

                # Realizando o reembolso do cliente
                obj_refund = stripe.Refund.create(
                    payment_intent=payment_intent, 
                    amount=int(pagamento_evento.preco_pedido * 100),
                    metadata={
                        'id_pagamento': pagamento_evento.id,
                    }
                )
                id_refund = obj_refund.get('id')

                pagamento_evento.payment_intent = payment_intent
                pagamento_evento.id_reembolso = id_refund
                pagamento_evento.status_pedido = 'refund'
                pagamento_evento.save()

                if pagamento_evento.evento.tipo == 'Presencial':
                    link = f'{DOMINIO}/eventos/presenciais/'
                else:
                    link = f'{DOMINIO}/eventos/online/'
                
                # Enviando E-mail - Início
                html_content = render_to_string('emails/reembolso_feito_email.html', 
                {'nome_perfil': pagamento_evento.perfil.nome, 
                'preco': pagamento_evento.preco_pedido,
                'nome_evento': pagamento_evento.evento.nome,
                'data': pagamento_evento.evento.data,
                'link': link})
                text_content = strip_tags(html_content)

                _email = EmailMultiAlternatives(f'Você recebeu um reembolso', text_content, 
                settings.EMAIL_HOST_USER, [pagamento_evento.perfil.usuario.email])
                _email.attach_alternative(html_content, 'text/html')
                _email.send()
                # Enviando E-mail - Fim 
                pagamento_evento.recebeu_email_refund = True
                pagamento_evento.save()

                return HttpResponse(status=200)

                """ evento.qtd_participantes =- 1
                evento.save() """
            else:
                if evento.divisao_genero != 'metade':
                    evento.qtd_participantes-=qtd_participantes_pago
                elif perfil.genero == 'Masculino':
                    evento.qtd_participantes_homens-=qtd_participantes_pago
                else:
                    evento.qtd_participantes_mulheres-=qtd_participantes_pago
                evento.save()
            # Verificando se o evento já esgotou - Fim

            pagamento_evento.payment_intent = payment_intent
            pagamento_evento.pagamento_feito = True
            pagamento_evento.status_pedido = 'approved'

            participante_evento = ParticipantesEvento.objects.create(remetente=perfil, evento=evento, confirmacao='Confirmado')
            participante_evento.save()

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
            participante_evento.codigo = codigo
            participante_evento.img_qrcode = qr_code_file
            participante_evento.link_confirmacao = f'{link_confirmacao}/{codigo}/'
            participante_evento.save()
            # Gerando o QR Code e o Link - Fim

            # Gerando o Bilhete - Início
            if evento.tipo == 'Presencial':
                template_path = BASE_DIR / 'templates' / 'docs' / 'documento_evento_presencial.docx'

                replacements = {
                    '{EVENT_NAME}': evento.nome,
                    '{PERFIL_NAME}': perfil.nome,
                    '{DATA_EVENTO}': evento.data.strftime('%d/%m/%Y %H:%M:%S'),
                    '{VALOR_EVENTO}': str(pagamento_evento.preco_pedido),
                    '{LOCALIZACAO}': evento.localizacao,
                    '{QTD_CRIANCAS}': str(pagamento_evento.qtd_criancas),
                }
            else:
                template_path = BASE_DIR / 'templates' / 'docs' / 'documento_evento_online.docx'

                replacements = {
                    '{EVENT_NAME}': evento.nome,
                    '{PERFIL_NAME}': perfil.nome,
                    '{DATA_EVENTO}': evento.data.strftime('%d/%m/%Y %H:%M:%S'),
                    '{VALOR_EVENTO}': str(pagamento_evento.preco_pedido),               
                    '{LINK_REUNIAO}': evento.link_reuniao,
                    '{QTD_CRIANCAS}': str(pagamento_evento.qtd_criancas),
                }

            images = {
                '{IMAGE_PLACEHOLDER}': 
                {
                    'path': participante_evento.img_qrcode.path,
                    'width': Inches(2),  # Specify width as 2 inches
                    'height': Inches(2)  # Specify height as 2 inches
                }
            }

            temp_file = create_confirmation_ticket(template_path, replacements, images) # Abra o arquivo temporário como um objeto Django File
            temp_file.seek(0)  # Move o ponteiro do arquivo para o início
            django_file = File(temp_file, name='bilhete_de_confirmacao_final.docx')
            participante_evento.bilhete.save('bilhete_de_confirmacao_final.docx', django_file) # Salva o arquivo no modelo
            temp_file.close() # Fecha e remove o arquivo temporário
            participante_evento.save()

            # Gerando o Bilhete - Fim

            if evento.localizacao:
                localizacao = evento.localizacao
            else:
                localizacao = 'vazio'

            if evento.link_localizacao:
                link_localizacao = evento.link_localizacao
            else:
                link_localizacao = 'vazio'
            
            if not pagamento_evento.recebeu_email_aprovado:
                # Enviando E-mail - Início
                html_content = render_to_string('emails/pagamento_evento_confirmado.html', 
                {'nome_evento': evento.nome, 
                 'descricao': evento.descricao, 
                'nome_perfil': perfil.nome,
                'preco': pagamento_evento.preco_pedido,
                'localizacao': localizacao,
                'link_localizacao': link_localizacao,
                'tipo_evento': evento.tipo,
                'data': evento.data,
                'qtd_criancas': pagamento_evento.qtd_criancas,
                'link': f'{DOMINIO}/perfil/meus_eventos/'})
                text_content = strip_tags(html_content)

                _email = EmailMultiAlternatives(f'Você confirmou o seu convite para o evento "{evento.nome}"', text_content, 
                settings.EMAIL_HOST_USER, [perfil.usuario.email])
                _email.attach_alternative(html_content, 'text/html')
                _email.send()
                # Enviando E-mail - Fim 
                pagamento_evento.recebeu_email_aprovado = True

            participante_evento.save()
            pagamento_evento.save()

            # Se esse perfil teve convites, o remetente receberá a confirmação
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

        else:
            return HttpResponse(status=416)

    # Mandando o e-mail pro cliente que recebeu o reembolso
    """ elif event_type == "charge.refunded":
        with open('E:\\Projetos Visual Code\\Python_Freelancer\\FINDB\\payment\\log.txt', 'a+', encoding='utf-8') as file:
            file.write(f'{event} \n')

        try:
            id_pagamento = event.get('data').get('object').get('metadata')['id_pagamento']
        except:
            return HttpResponse(status=412)
        
        if PagamentoEventos.objects.filter(id=id_pagamento).exists():
            pagamento_evento = PagamentoEventos.objects.get(id=id_pagamento)

            if pagamento_evento.evento.tipo == 'Presencial':
                link = f'{DOMINIO}/eventos/presenciais/'
            else:
                link = f'{DOMINIO}/eventos/online/'

            # Enviando E-mail - Início
            html_content = render_to_string('emails/reembolso_feito_email.html', 
            {'nome_perfil': pagamento_evento.perfil.nome, 
            'preco': pagamento_evento.preco_pedido,
            'nome_evento': pagamento_evento.evento.nome,
            'data': pagamento_evento.evento.data,
            'link': link})
            text_content = strip_tags(html_content)

            _email = EmailMultiAlternatives(f'Você recebeu um reembolso', text_content, 
            settings.EMAIL_HOST_USER, [pagamento_evento.perfil.usuario.email])
            _email.attach_alternative(html_content, 'text/html')
            _email.send()
            # Enviando E-mail - Fim 
            pagamento_evento.status_pedido = 'refund'
            pagamento_evento.recebeu_email_refund = True
            pagamento_evento.save()

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=413)
    else:
        return HttpResponse(status=411) """
    


# Atualizar preços das assinaturas - Início
def list_all_subscriptions():
    all_subscriptions = []
    last_subscription = None
    
    while True:
        # Limite de assinaturas
        params = {'limit': 1000}
        if last_subscription:
            params['starting_after'] = last_subscription['id']
        
        # Lista todas as assinaturas - por padrão, retorna 10, por isso temos que fazer a paginação e extrair tudo
        subscriptions = stripe.Subscription.list(**params)
        all_subscriptions.extend(subscriptions['data'])
        
        if not subscriptions['has_more']:
            break
        
        last_subscription = subscriptions['data'][-1]
    
    return all_subscriptions


def atualizar_preco(request):
    stripe.api_key = KEY_SECRET_STRIPE

    # Crie o produto manualmente lá na dashboard da stripe
    # https://dashboard.stripe.com/test/products
    # Pegue o id do produto criado, e atualize as assinaturas
    # OBS: quando muda a assinatura, o id_assinatura e id_customer não mudam

    new_id_price = 'price_1PjjCmJzt0o0PZfSS4GEyL22'

    try:
        new_product = stripe.Price.retrieve(new_id_price)
        new_price_id = new_product.get('id')
        new_price = new_product.get('unit_amount')
        if len(f'{new_price}') == 3:
            new_price = new_price / 10
        elif len(f'{new_price}') >= 4:
            new_price = new_price / 100
    except:
        messages.error(request, f'O código enviado: "{new_id_price}" não está atrelado a nenhum produto na sua conta stripe. Verifique o código certo')
        return redirect('planos')
    
    # return HttpResponse(f'{new_price} - {type(new_price)}')

    # tipo = 'tres_meses'
    # tipo = 'seis_meses'
    tipo = 'doze_meses'

    if tipo != 'tres_meses' and tipo != 'seis_meses' and tipo != 'doze_meses':
        messages.error(request, f'O valor mandado: "{tipo}" não é um plano válido.')
        return redirect('planos')

    # Todos os planos tem que existir para prosseguir
    if not Plano.objects.filter(nome='tres_meses').exists() and not Plano.objects.filter(nome='seis_meses').exists() and not Plano.objects.filter(nome='doze_meses').exists():
        messages.error(request, f'Nem todos os planos foram cadastrados ainda. Fale com o suporte.')
        return redirect('planos')

    # Na sua dashboard, criar em catalogo de produtos as assinaturas com pagamento recorrente
    # Pegar o código do produto e colocar aqui
    codigo_tres_meses = Plano.objects.filter(nome='tres_meses').first().codigo
    codigo_seis_meses = Plano.objects.filter(nome='seis_meses').first().codigo
    codigo_doze_meses = Plano.objects.filter(nome='doze_meses').first().codigo

    """ assinaturas = list_all_subscriptions()
    for assinatura in assinaturas:
        # Pega o id da assinatura e o id do produto antigo
        id_assinatura = assinatura.get('id')
        current_period_end = assinatura.get('current_period_end')
        customer = assinatura.get('customer')
        old_id_price = assinatura.get('items').get('data')[0].get('price').get('id')
        id_items_assinatura = assinatura.get('items').get('data')[0].get('id')
        # Verifica qual assinatura o admin escolheu pra atualizar
        if old_id_price == codigo_tres_meses and tipo == 'tres_meses':
            print('tres_meses')
            if Pedido.objects.filter(id_user=customer).exists():
                pedido = Pedido.objects.get(id_user=customer)
                pedido.preco_pedido = new_price
                pedido.current_period_end = current_period_end
                pedido.save()

            stripe.Subscription.modify(
                id_assinatura,
                items=[{
                    'id': id_items_assinatura,
                    'price': new_price_id,  # ID do novo preço
                }]
            )
        elif old_id_price == codigo_seis_meses and tipo == 'seis_meses':
            print('seis_meses')
            if Pedido.objects.filter(id_user=customer).exists():
                pedido = Pedido.objects.get(id_user=customer)
                pedido.preco_pedido = new_price
                pedido.current_period_end = current_period_end
                pedido.save()

            stripe.Subscription.modify(
                id_assinatura,
                items=[{
                    'id': id_items_assinatura,
                    'price': new_price_id,  # ID do novo preço
                }]
            )
        elif old_id_price == codigo_doze_meses and tipo == 'doze_meses':
            stripe.Subscription.modify(
                id_assinatura,
                items=[{
                    'id': id_items_assinatura,
                    'price': new_price_id,  # ID do novo preço
                }],
                metadata={
                    'upgrade': True,
                },
            )

            if Pedido.objects.filter(id_assinatura=id_assinatura).exists():
                print('/////////////////////////////////////')
                pedido = Pedido.objects.get(id_assinatura=id_assinatura)
                print(new_price)
                pedido.preco_pedido = new_price
                print(pedido.preco_pedido)
                pedido.current_period_end = current_period_end
                pedido.save()
                print(pedido.preco_pedido) """
        
    if not Pedido.objects.filter(plano_ativo=True).exists():
        messages.error(request, f'O site, atualmente não tem nenhum plano ativo.')
        return redirect('planos')
    
    if tipo == 'tres_meses':
        _plano = Plano.objects.filter(nome='tres_meses').first()
    elif tipo == 'seis_meses':
        _plano = Plano.objects.filter(nome='seis_meses').first()
    elif tipo == 'doze_meses':
        _plano = Plano.objects.filter(nome='doze_meses').first()
    else:
        messages.error(request, f'O valor mandado: "{tipo}" não é um plano válido.')
        return redirect('planos')
    _plano.codigo = new_price_id
    _plano.preco = new_price
    _plano.save()

    assinaturas = Pedido.objects.filter(plano_ativo=True)
    for assinatura in assinaturas:
        data = stripe.Subscription.retrieve(assinatura.id_assinatura)
        if not data:
            continue
        id_assinatura = data.get('id')
        # current_period_end = data.get('current_period_end')
        # customer = data.get('customer')
        old_id_price = data.get('items').get('data')[0].get('price').get('id')
        id_items_assinatura = data.get('items').get('data')[0].get('id')

        validador = False
        print(old_id_price)
        print(codigo_tres_meses)
        print(codigo_seis_meses)
        print(codigo_doze_meses)
        print('=============')
        if old_id_price == codigo_tres_meses and tipo == 'tres_meses':
            validador = True
        elif old_id_price == codigo_seis_meses and tipo == 'seis_meses':
            validador = True
        elif old_id_price == codigo_doze_meses and tipo == 'doze_meses':
            validador = True

        print(assinatura.id_assinatura)
        print(id_assinatura)
        print(assinatura.id_assinatura == id_assinatura)
        print(validador)
        print('-------------------')

        if validador:
            print('MUDOU')
            stripe.Subscription.modify(
                id_assinatura,
                items=[{
                    'id': id_items_assinatura,
                    'price': new_price_id,  # ID do novo preço
                }],
                metadata={
                    'perfil_slug': assinatura.perfil.slug,
                    'plano_codigo': new_price_id,
                    'upgrade': True,
                },
            )

    return HttpResponse('oi')

# Atualizar preços das assinaturas - Fim