from django.utils import timezone
from .models import Perfil
from django.shortcuts import redirect

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.user.is_authenticated and 
            Perfil.objects.filter(usuario=request.user).exists() and not 
            request.path.startswith('/comunication/get_comunications/') and not 
            request.path.startswith('/comunication/get_comunication/')):
            perfil = Perfil.objects.get(usuario=request.user)
            perfil.last_activity = timezone.now()
            perfil.save()
        response = self.get_response(request)
        return response
    

class LoginAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/admin/login/'):
            return redirect('login')
        response = self.get_response(request)
        return response
