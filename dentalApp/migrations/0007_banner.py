# Generated by Django 5.1.4 on 2025-01-13 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dentalApp', '0006_socialmediasettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(upload_to='banners/')),
            ],
        ),
    ]
