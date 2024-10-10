from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Evento, ParticipantesEvento
import os

""" @receiver(post_delete, sender=Evento)
def delete_foto_video_evento_pos(sender, instance, *args, **kwargs):
    old_instance = Evento.objects.get(id=instance.id)
    if old_instance.foto:
        os.remove(old_instance.foto.path)

    if old_instance.video2:
        os.remove(old_instance.video2.path) """


@receiver(pre_delete, sender=Evento)
def delete_foto_video_evento_pre(sender, instance, *args, **kwargs):
    if instance.foto:
        os.remove(instance.foto.path)

    if instance.video2:
        os.remove(instance.video2.path)


@receiver(pre_delete, sender=ParticipantesEvento)
def delete_arquivos_participacao_evento(sender, instance, *args, **kwargs):
    old_instance = ParticipantesEvento.objects.get(id=instance.id)

    if old_instance.bilhete:
        os.remove(old_instance.bilhete.path)
    if old_instance.img_qrcode:
        os.remove(old_instance.img_qrcode.path)



