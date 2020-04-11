# Generated by Django 3.0.3 on 2020-04-11 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(blank='True', max_length=200)),
                ('keywords', models.CharField(blank='True', max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('address', models.CharField(blank='True', max_length=200)),
                ('phone', models.CharField(blank='True', max_length=15)),
                ('fax', models.CharField(blank='True', max_length=15)),
                ('email', models.CharField(max_length=50)),
                ('smtpserver', models.CharField(max_length=20)),
                ('smtpemail', models.CharField(max_length=20)),
                ('smtppassword', models.CharField(max_length=10)),
                ('smtpport', models.CharField(max_length=5)),
                ('icon', models.ImageField(blank='True', upload_to='images/')),
                ('facebook', models.CharField(max_length=20)),
                ('twitter', models.CharField(max_length=20)),
                ('instagram', models.CharField(max_length=20)),
                ('aboutus', models.TextField()),
                ('reference', models.TextField()),
                ('status', models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], max_length=10)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
