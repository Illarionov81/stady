# Generated by Django 2.2.13 on 2021-02-04 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20210204_2117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='tag',
            new_name='tags',
        ),
    ]
