from datetime import datetime, timedelta
from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='format_timestamp')
def format_timestamp(timestamp):
    date_time = datetime.fromtimestamp(timestamp)
    return date_time

@register.filter(name='format_plan')
def format_plan(plan):
    return plan.replace('_', ' ').title()

@register.filter(name='format_name_plan')
def format_name_plan(plan):
    if plan == 'approved':
        return 'Aprovada'
    elif plan == 'cancel':
        return 'Cancelada'
    elif plan == 'paused':
        return 'Pausada'
    elif plan == 'rejected':
        return 'Rejeitada'
    elif plan == 'pending':
        return 'Pendente'
    

@register.filter(name='is_user_online')
def is_user_online(perfil):
    if not perfil.last_activity:
        return False
    now = timezone.now()
    online_threshold = now - timedelta(minutes=5)
    return True if perfil.last_activity >= online_threshold else False
    
