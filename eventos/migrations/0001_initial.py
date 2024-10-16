# Generated by Django 5.0.6 on 2024-07-29 01:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
                ('nome', models.CharField(default='', max_length=300, verbose_name='Nome')),
                ('slug', models.SlugField(default='', max_length=255, unique=True, verbose_name='Slug')),
                ('codigo', models.CharField(default='', max_length=255, verbose_name='Código')),
                ('descricao', models.TextField(default='', max_length=10000, verbose_name='Descrição')),
                ('tipo', models.CharField(choices=[('Presencial', 'Presencial'), ('Online', 'Online')], default='Presencial', max_length=255, verbose_name='Tipo')),
                ('pagamento', models.CharField(choices=[('Gratuito', 'Gratuito'), ('Pago', 'Pago')], default='Gratuito', max_length=255, verbose_name='Pagamento')),
                ('valor', models.FloatField(default=0, verbose_name='Valor')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='eventos_fotos/%Y/%m/%d', verbose_name='Foto')),
                ('localizacao', models.CharField(default='', max_length=1000, verbose_name='Localização')),
                ('link_localizacao', models.URLField(default='', max_length=3000, verbose_name='Link Localização')),
                ('link_reunião', models.CharField(default='', max_length=3000, verbose_name='Link Reunião')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
            },
        ),
    ]
