# Generated by Django 4.2.3 on 2024-05-02 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop',
            name='Area',
        ),
    ]
