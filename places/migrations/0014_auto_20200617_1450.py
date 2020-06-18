# Generated by Django 3.0.3 on 2020-06-17 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0013_auto_20200617_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='currency',
            field=models.CharField(choices=[('₺', 'Türk Lirası'), ('$', 'Dolar'), ('€', 'Euro')], max_length=10),
        ),
    ]
