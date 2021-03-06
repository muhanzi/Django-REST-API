# Generated by Django 3.1.2 on 2021-10-02 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_module', '0005_auto_20210924_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='status',
            field=models.CharField(default='initiated', max_length=255),
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(default='sent', max_length=255),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(default='pending', max_length=255),
        ),
    ]
