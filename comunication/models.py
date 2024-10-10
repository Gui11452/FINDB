from django.db import models
from perfil.models import Perfil
from django.utils import timezone

class Comunication(models.Model):
    remetente = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comunication_remetente', verbose_name='Remetente')
    destinatario = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comunication_destinatario', verbose_name='Destinatário')
    tipo = models.CharField(
        default='video',
        max_length=255, 
        verbose_name="audio", 
        choices=[
            ("audio", "audio"),
            ("video", "video"),
        ],
    )

    confirmacao = models.CharField(
        default='Pendente',
        max_length=255, 
        verbose_name="Confirmação", 
        choices=[
            ("Pendente", "Pendente"),
            ("Expirado", "Expirado"),
            ("Rejeitado", "Rejeitado"),
            ("Confirmado", "Confirmado"),
        ],
    )

    data = models.DateTimeField(default=timezone.now, verbose_name='Data')

    codigo = models.CharField(default='', max_length=2000, verbose_name='Código')

    class Meta:
        verbose_name = 'Comunication'
        verbose_name_plural = 'Comunications'

    def __str__(self):
        return f'{self.remetente} -> {self.destinatario} -> {self.tipo}'
    

class BloquearUsuarios(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='perfil_usuario', verbose_name='Remetente')
    bloqueado = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='perfil_bloqueado', verbose_name='Destinatário')

    class Meta:
        verbose_name = 'Bloquear Usuário'
        verbose_name_plural = 'Bloquear Usuários'

    def __str__(self):
        return f'{self.usuario} -> {self.bloqueado}'
