# Generated by Django 5.0.6 on 2024-07-26 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0009_alter_cupido_codigo_alter_perfil_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupido',
            name='nome',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nome'),
        ),
    ]
