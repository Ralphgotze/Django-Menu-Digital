# Generated by Django 5.1.1 on 2024-11-22 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0007_rename_category_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrito',
            name='atendido',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='carrito',
            name='enviado',
            field=models.BooleanField(default=False),
        ),
    ]
