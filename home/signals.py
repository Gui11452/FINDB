from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Carrossel
import os

@receiver(pre_delete, sender=Carrossel)
def delete_banners_carrossel(sender, instance, *args, **kwargs):
    old_instance = Carrossel.objects.get(id=instance.id)

    if old_instance.banner1:
        os.remove(old_instance.banner1.path)
    if old_instance.banner2:
        os.remove(old_instance.banner2.path)
    if old_instance.banner3:
        os.remove(old_instance.banner3.path)