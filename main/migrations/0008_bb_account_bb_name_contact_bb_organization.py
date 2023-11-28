# Generated by Django 4.2.6 on 2023-11-26 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_advuser_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='account',
            field=models.CharField(default='Не указан??????', max_length=40, verbose_name='Тип учётной записи'),
        ),
        migrations.AddField(
            model_name='bb',
            name='name_contact',
            field=models.CharField(default='Не указано', max_length=100, verbose_name='ФИО соискателя'),
        ),
        migrations.AddField(
            model_name='bb',
            name='organization',
            field=models.CharField(default='Не указано', max_length=100, verbose_name='Название организации'),
        ),
    ]