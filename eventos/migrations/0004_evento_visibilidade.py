# Generated by Django 5.0.6 on 2024-07-29 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_conviteevento_notificacao_participantesevento'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='visibilidade',
            field=models.BooleanField(default=True, verbose_name='Visibilidade'),
        ),
    ]
