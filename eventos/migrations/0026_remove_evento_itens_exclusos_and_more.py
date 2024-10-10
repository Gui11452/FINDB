# Generated by Django 5.0.6 on 2024-08-09 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0025_remove_evento_itens_exclusos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='itens_exclusos',
        ),
        migrations.RemoveField(
            model_name='evento',
            name='itens_inclusos',
        ),
        migrations.AddField(
            model_name='evento',
            name='itens_exclusos',
            field=models.ManyToManyField(blank=True, related_name='itens_exclusos', to='eventos.item', verbose_name='Itens NÃO Inclusos*'),
        ),
        migrations.AddField(
            model_name='evento',
            name='itens_inclusos',
            field=models.ManyToManyField(blank=True, related_name='itens_inclusos', to='eventos.item', verbose_name='Itens Inclusos*'),
        ),
    ]
