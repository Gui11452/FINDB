from django.db import models


class Carrossel(models.Model):
    banner1 = models.ImageField(blank=True, null=True, upload_to='banner_home/%Y/%m/%d', verbose_name="Banner 1")
    link1 = models.URLField(blank=True, null=True, max_length=3000, verbose_name="Link 1")

    banner2 = models.ImageField(blank=True, null=True, upload_to='banner_home/%Y/%m/%d', verbose_name="Banner 2")
    link2 = models.URLField(blank=True, null=True, max_length=3000, verbose_name="Link 2")

    banner3 = models.ImageField(blank=True, null=True, upload_to='banner_home/%Y/%m/%d', verbose_name="Banner 3")
    link3 = models.URLField(blank=True, null=True, max_length=3000, verbose_name="Link 3")


    class Meta:
        verbose_name = 'Carrossel'
        verbose_name_plural = 'Carrossel'

    def __str__(self):
        return f'{self.banner1} - {self.banner2} - {self.banner3}'
