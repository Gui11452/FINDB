# Generated by Django 5.0.6 on 2024-07-30 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0018_alter_perfil_interesse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='interesse',
            field=models.CharField(choices=[('Networking', 'Networking'), ('Terapias diversas', 'Terapias diversas'), ('Profissionais em relacionamento', 'Profissionais em relacionamento'), ('Eventos', 'Eventos'), ('Relacionamento Sério', 'Relacionamento Sério'), ('Encontros', 'Encontros'), ('Namoros', 'Namoros'), ('Amizades', 'Amizades')], default='Relacionamento Sério', max_length=255, verbose_name='Interesses'),
        ),
    ]
