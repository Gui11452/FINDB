# Generated by Django 5.0.6 on 2024-07-30 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0017_rename_link_reunião_videochamada_link_reuniao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='interesse',
            field=models.CharField(choices=[('Networking', 'Networking'), ('Terapias diversas', 'Terapias diversas'), ('Profissionais em relacionamento', 'Profissionais em relacionamento'), ('Eventos', 'Eventos'), ('Não quero relacionamentos', 'Não quero relacionamentos'), ('Relacionamento Sério', 'Relacionamento Sério'), ('Encontros', 'Encontros'), ('Namoros', 'Namoros'), ('Amizades', 'Amizades')], default='Relacionamento Sério', max_length=255, verbose_name='Interesses'),
        ),
    ]
