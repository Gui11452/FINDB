from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Perfil, Album, Cupido, ColaboradoresEvento
import os

""" @receiver(post_save, sender=Perfil)
def alter_foto_cupido(sender, instance, *args, **kwargs):
    # old_perfil = Perfil.objects.get(id=instance.id)

    if Cupido.objects.filter(usuario=instance.usuario).exists():
        cupido = Cupido.objects.get(usuario=instance.usuario)
        if instance.foto:
            cupido.foto = instance.foto
            cupido.save() """


@receiver(post_delete, sender=Perfil)
def delete_foto_cupido(sender, instance, *args, **kwargs):
    if Cupido.objects.filter(usuario=instance.usuario).exists():
        cupido = Cupido.objects.get(usuario=instance.usuario)
        if cupido.foto:
            caminho = cupido.foto.path
            cupido.foto = None
            cupido.save()
            os.remove(caminho)


@receiver(post_delete, sender=Perfil)
def delete_perfil_user(sender, instance, *args, **kwargs):
    instance.usuario.delete()

@receiver(post_delete, sender=ColaboradoresEvento)
def delete_colaborador_evento_user(sender, instance, *args, **kwargs):
    instance.usuario.delete()

@receiver(pre_delete, sender=Album)
def delete_album_fotos(sender, instance, *args, **kwargs):
    old_instance = Album.objects.get(id=instance.id)

    if old_instance.foto1:
        os.remove(old_instance.foto1.path)
    if old_instance.foto2:
        os.remove(old_instance.foto2.path)
    if old_instance.foto3:
        os.remove(old_instance.foto3.path)
    if old_instance.foto4:
        os.remove(old_instance.foto4.path)
    if old_instance.foto5:
        os.remove(old_instance.foto5.path)


@receiver(pre_delete, sender=Perfil)
def delete_foto_perfil(sender, instance, *args, **kwargs):
    old_instance = Perfil.objects.get(id=instance.id)

    if old_instance.foto:
        os.remove(old_instance.foto.path)

    