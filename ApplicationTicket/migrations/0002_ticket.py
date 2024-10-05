# Generated by Django 5.0.7 on 2024-09-22 21:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApplicationTicket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_beneficiaire', models.CharField(max_length=100)),
                ('prenom_beneficiaire', models.CharField(max_length=100)),
                ('email_beneficiaire', models.EmailField(max_length=254)),
                ('numero_whatsapp', models.CharField(max_length=15)),
                ('qr_code', models.ImageField(blank=True, upload_to='qrcodes/')),
                ('evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApplicationTicket.evenement')),
            ],
        ),
    ]
