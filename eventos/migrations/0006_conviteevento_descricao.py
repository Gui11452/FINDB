# Generated by Django 5.0.6 on 2024-07-29 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_alter_notificacao_convite_evento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conviteevento',
            name='descricao',
            field=models.TextField(default='', max_length=2000, verbose_name='Descrição'),
        ),
    ]
