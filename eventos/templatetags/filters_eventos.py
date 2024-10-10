from datetime import datetime
from django import template
from perfil.models import Perfil

register = template.Library()

@register.filter(name='format_homem_participantes_evento')
def format_homem_participantes_evento(qtd):
    if qtd != 1:
        return f'{int(qtd)} homens'
    else:
        return f'{int(qtd)} homem'
    
@register.filter(name='format_mulher_participantes_evento')
def format_mulher_participantes_evento(qtd):
    if qtd != 1:
        return f'{int(qtd)} mulheres'
    else:
        return f'{int(qtd)} mulher'
    
@register.filter(name='format_metade_participantes_evento')
def format_metade_participantes_evento(qtd):
    qtd = int(qtd / 2)
    if qtd == 1:
        return f'{qtd} homem e {qtd} mulher'
    else:
        return f'{qtd} homens e {qtd} mulheres'
    
@register.filter(name='format_pessoa_participantes_evento')
def format_pessoa_participantes_evento(qtd):
    if qtd != 1:
        return f'{int(qtd)} pessoas'
    else:
        return f'{int(qtd)} pessoa'
    
@register.filter(name='format_ano')
def format_ano(qtd):
    if qtd != 1:
        return f'{int(qtd)} anos'
    else:
        return f'{int(qtd)} ano'
    

    
