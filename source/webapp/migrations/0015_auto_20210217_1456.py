# Generated by Django 2.2.13 on 2021-02-17 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_auto_20210205_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
    ]