# Generated by Django 5.0.6 on 2024-08-03 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0021_perfil_codigo_cancelar_assinatura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videochamada',
            name='link_reuniao',
            field=models.CharField(blank=True, default='', max_length=3000, null=True, verbose_name='Link Reunião'),
        ),
    ]
