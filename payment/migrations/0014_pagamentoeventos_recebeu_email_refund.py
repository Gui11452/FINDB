# Generated by Django 5.0.6 on 2024-08-05 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_pagamentoeventos_id_reembolso'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamentoeventos',
            name='recebeu_email_refund',
            field=models.BooleanField(default=False, verbose_name='Código Interno REF'),
        ),
    ]
