# Generated by Django 5.2 on 2025-05-05 17:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kvitsapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='attels',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='ean13',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Uzņēmuma nosaukums')),
                ('registration_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Reģistrācijas numurs')),
                ('vat_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='PVN numurs')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adrese')),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Telefona numurs')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
