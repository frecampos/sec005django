# Generated by Django 3.2 on 2021-05-18 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misPerris', '0004_mascota_publicar'),
    ]

    operations = [
        migrations.AddField(
            model_name='mascota',
            name='comentario',
            field=models.TextField(default='--'),
        ),
    ]
