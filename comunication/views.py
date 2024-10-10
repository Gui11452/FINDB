from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from perfil.models import Perfil
from .models import BloquearUsuarios, Comunication
from payment.models import Pedido
import string, random
from django.contrib import messages
from namoro.settings import ZEGOCLOUD_VIDEO_API_KEY, ZEGOCLOUD_VIDEO_SERVER_SECRET, DOMINIO, ZEGOCLOUD_AUDIO_SERVER_SECRET, ZEGOCLOUD_AUDIO_API_KEY
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

def send_notification_comunication(request):
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if request.method != 'POST':
        return redirect(http_referer)
    
    slug_destinatario = request.POST.get('slug_destinatario')
    tipo = request.POST.get('tipo')

    if not request.user.is_authenticated or not Perfil.objects.filter(usuario=request.user, verificacao_email=True):
        return redirect('login')
    remetente = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    # Verificação da assinatura - Início
    if not Pedido.objects.filter(perfil=remetente, plano_ativo=True).exists():
        messages.error(request, f'Você não tem nenhuma assinatura ativa.')
        return redirect('planos')
    # Verificação da assinatura - Fim

    if not Perfil.objects.filter(slug=slug_destinatario, verificacao_email=True).exists():
        return redirect('home')

    destinatario = Perfil.objects.get(slug=slug_destinatario, verificacao_email=True)

    if BloquearUsuarios.objects.filter(usuario=destinatario, bloqueado=remetente).exists():
        messages.error(request, f'Você não pode convidar "{destinatario.nome}", pois você foi bloqueado.')
        return redirect(http_referer)

    letras = string.ascii_letters
    digitos = string.digits
    geral = letras + digitos
    roomID = ''.join(random.choices(geral, k=20))

    comunication = Comunication.objects.create(
        remetente=remetente,
        destinatario=destinatario,
        tipo=tipo,
    )
    comunication.save()
    
    # Envia a mensagem para o grupo de notificações
    obj = {
        'id': comunication.id,
        'destinatario_nome': destinatario.nome,
        'destinatario_foto': destinatario.foto.url if destinatario.foto else '/static/images/foto_user.png',
        'link_destinatario': f'{DOMINIO}/perfil/info/{destinatario.slug}/',
        'roomID': roomID,
        'tipo': tipo,
    }

    # return JsonResponse({'status': 'success', 'message': 'Notificação enviada!'})
    return render(request, 'send_notification_call.html', obj)


def comunication_call(request, roomID):
    if not request.user.is_authenticated or not Perfil.objects.filter(usuario=request.user, verificacao_email=True):
        messages.error(request, 'Você precisa estar online para acessar essa página')
        return redirect('login')
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not Comunication.objects.filter(
        Q(
            Q(remetente=perfil) |
            Q(destinatario=perfil), 
        ), 
        codigo=roomID,
    ).exists():
        return JsonResponse({'error': 'Essa chamada não existe ou o usuário logado não tem acesso a essa chamada.'})

    comunication = Comunication.objects.get(
        Q(
            Q(remetente=perfil) |
            Q(destinatario=perfil), 
        ), 
        codigo=roomID,
    )

    if comunication.tipo == 'audio':
        return render(request, 'audio_call.html', {
            'roomID': roomID,
            'ZEGOCLOUD_AUDIO_API_KEY': ZEGOCLOUD_AUDIO_API_KEY,
            'ZEGOCLOUD_AUDIO_SERVER_SECRET': ZEGOCLOUD_AUDIO_SERVER_SECRET,
            'perfil_nome': perfil.nome,
            'perfil_slug': perfil.slug,
        })
    else:
        return render(request, 'video_call.html', {
            'roomID': roomID,
            'ZEGOCLOUD_VIDEO_API_KEY': ZEGOCLOUD_VIDEO_API_KEY,
            'ZEGOCLOUD_VIDEO_SERVER_SECRET': ZEGOCLOUD_VIDEO_SERVER_SECRET,
            'perfil_nome': perfil.nome,
            'perfil_slug': perfil.slug,
        })



def get_comunications(request, slug_perfil):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'usuário offline'})
    
    if not Perfil.objects.filter(slug=slug_perfil, verificacao_email=True).exists():
        return JsonResponse({'error': 'perfil nao encontrado.'})

    perfil = Perfil.objects.get(slug=slug_perfil, verificacao_email=True)

    um_minuto_atras = timezone.now() - timedelta(minutes=1)

    comunications_expired = Comunication.objects.filter(
        destinatario=perfil, 
        confirmacao='Pendente', 
        data__lte=um_minuto_atras
    )
    for comunication_expired in comunications_expired:
        comunication_expired.confirmacao = 'Expirado'
        comunication_expired.save()

    if not Comunication.objects.filter(
        destinatario=perfil, 
        confirmacao='Pendente', 
        data__gte=um_minuto_atras
    ).exists():
        return JsonResponse({'error': 'esse perfil nao esta recebendo nenhuma comunicacao no momento.'})

    comunications = Comunication.objects.filter(
        destinatario=perfil, 
        confirmacao='Pendente',
        data__gte=um_minuto_atras
    )
    
    info = {}
    validador_block = False
    for comunication in comunications:
        if BloquearUsuarios.objects.filter(usuario=perfil, bloqueado=comunication.remetente).exists():
            # return JsonResponse({'error': 'o destinatário bloqueou o remetente'})
            validador_block = True
            continue
        info[comunication.id] = {
            'id': comunication.id,
            'confirmacao': comunication.confirmacao,
            'remetente_slug': comunication.remetente.slug,
            'remetente_nome': comunication.remetente.nome,
            'remetente_genero': comunication.remetente.genero,
            'remetente_foto': comunication.remetente.foto.url if comunication.remetente.foto else '/static/images/foto_user.png',
            'link_remetente': f'{DOMINIO}/perfil/info/{comunication.remetente.slug}/',
            'roomID': comunication.codigo,
            'tipo': comunication.tipo,
        }
    
    if not info and validador_block:
        return JsonResponse({'error': 'o destinatário bloqueou o remetente'})
    else:
        return JsonResponse(info)


def get_comunication(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'usuário offline'})
    
    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        return JsonResponse({'error': 'O usuário logado não está atrelado a nenhum perfil.'})

    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not Comunication.objects.filter(id=id, remetente=perfil).exists():
        return JsonResponse({'error': 'Essa chamada não existe ou o usuário logado não tem acesso a essa chamada.'})

    comunication = Comunication.objects.get(id=id, remetente=perfil)

    if BloquearUsuarios.objects.filter(usuario=comunication.destinatario, bloqueado=comunication.remetente).exists():
        return JsonResponse({'error': 'block', 'mensagem': f'O usuário "{comunication.destinatario}" te bloqueou.'})

    obj = {
        'id': comunication.id,
        'confirmacao': comunication.confirmacao,
        'roomID': comunication.codigo,
        'tipo': comunication.tipo,
    }
    
    return JsonResponse(obj)


def confirmar_chamada(request, id):
    if not request.user.is_authenticated:
        messages.error(request, f'Usuário offline')
        return redirect(http_referer)
    
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        messages.error(request, 'O usuário logado não está atrelado a nenhum perfil.')
        return redirect(http_referer)

    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not Comunication.objects.filter(id=id, destinatario=perfil).exists():
        messages.error(request, 'Você não tem acesso a essa chamada.')
        return redirect(http_referer)
    
    letras = string.ascii_letters
    digitos = string.digits
    geral = letras + digitos
    while True:
        codigo = ''.join(random.choices(geral, k=25))
        if not Comunication.objects.filter(codigo=codigo).exists():
            break

    comunication = Comunication.objects.get(id=id, destinatario=perfil)
    comunication.confirmacao = 'Confirmado'
    comunication.codigo = codigo
    comunication.save()

    messages.success(request, f'Você confirmou a chamada de "{comunication.remetente.nome}"')
    return redirect(f"{DOMINIO}/comunication/comunication_call/{codigo}/")


def rejeitar_chamada(request, id):
    if not request.user.is_authenticated:
        messages.error(request, f'Usuário offline')
        return redirect(http_referer)
    
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not Perfil.objects.filter(usuario=request.user, verificacao_email=True).exists():
        messages.error(request, 'O usuário logado não está atrelado a nenhum perfil.')
        return redirect(http_referer)

    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not Comunication.objects.filter(id=id, destinatario=perfil).exists():
        messages.error(request, 'Você não tem acesso a essa chamada.')
        return redirect(http_referer)

    comunication = Comunication.objects.get(id=id, destinatario=perfil)
    comunication.confirmacao = 'Rejeitado'
    comunication.save()

    messages.success(request, f'Você rejeitou a chamada de "{comunication.remetente.nome}"')
    return redirect(http_referer)



# Bloqueio/Desbloqueio usuários
def bloquear_usuario(request, slug_destinatario):
    if not request.user.is_authenticated:
        messages.error(request, f'Usuário offline')
        return redirect(http_referer)
    
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not request.user.is_authenticated or not Perfil.objects.filter(usuario=request.user, verificacao_email=True):
        return redirect('login')
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not Perfil.objects.filter(slug=slug_destinatario, verificacao_email=True).exists():
        return redirect('home')

    bloqueado = Perfil.objects.get(slug=slug_destinatario, verificacao_email=True)

    # Verificação bloqueio - Início
    if BloquearUsuarios.objects.filter(usuario=perfil, bloqueado=bloqueado).exists():
        messages.error(request, f'Você já bloqueou "{bloqueado.nome}".')
        return redirect(http_referer)
    # Verificação bloqueio - Fim

    obj_bloqueado = BloquearUsuarios.objects.create(usuario=perfil, bloqueado=bloqueado)
    obj_bloqueado.save()
    
    messages.success(request, f'Você bloqueou "{bloqueado.nome}".')
    return redirect(http_referer)


def desbloquear_usuario(request, slug_destinatario):
    if not request.user.is_authenticated:
        messages.error(request, f'Usuário offline')
        return redirect(http_referer)
    
    http_referer = request.META.get(
        'HTTP_REFERER',
        reverse('home')
    )

    if not request.user.is_authenticated or not Perfil.objects.filter(usuario=request.user, verificacao_email=True):
        return redirect('login')
    perfil = Perfil.objects.get(usuario=request.user, verificacao_email=True)

    if not Perfil.objects.filter(slug=slug_destinatario, verificacao_email=True).exists():
        return redirect('home')

    bloqueado = Perfil.objects.get(slug=slug_destinatario, verificacao_email=True)

    # Verificação bloqueio - Início
    if not BloquearUsuarios.objects.filter(usuario=perfil, bloqueado=bloqueado).exists():
        messages.error(request, f'Você não pode desbloquear "{bloqueado.nome}", pois ele não está bloqueado.')
        return redirect(http_referer)
    # Verificação bloqueio - Fim

    obj_bloqueado = BloquearUsuarios.objects.get(usuario=perfil, bloqueado=bloqueado)
    obj_bloqueado.delete()
    
    messages.success(request, f'Você desbloqueou "{bloqueado.nome}".')
    return redirect(http_referer)