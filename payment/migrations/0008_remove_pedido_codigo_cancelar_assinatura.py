# Generated by Django 5.0.6 on 2024-08-02 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_pedido_codigo_cancelar_assinatura'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='codigo_cancelar_assinatura',
        ),
    ]
