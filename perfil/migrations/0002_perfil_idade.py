# Generated by Django 5.0.6 on 2024-07-24 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='idade',
            field=models.IntegerField(default=0, verbose_name='Idade'),
        ),
    ]
