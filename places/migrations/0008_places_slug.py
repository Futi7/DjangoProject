# Generated by Django 3.0.3 on 2020-05-17 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0007_auto_20200412_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='slug',
            field=models.SlugField(blank='True', max_length=150),
        ),
    ]
