# Generated by Django 5.0.6 on 2024-05-18 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_order_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='avatar',
        ),
    ]