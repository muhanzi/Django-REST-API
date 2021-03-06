# Generated by Django 3.1.2 on 2021-09-23 21:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_module.recrutingagency'),
        ),
        migrations.AddField(
            model_name='employee',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 24, 0, 4, 23, 137462)),
        ),
        migrations.AddField(
            model_name='employee',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 24, 0, 4, 23, 137462)),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 24, 0, 4, 23, 136464)),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 24, 0, 4, 23, 136464)),
        ),
        migrations.AddField(
            model_name='supersite',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 24, 0, 4, 23, 137462)),
        ),
        migrations.AddField(
            model_name='supersite',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='supersite',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 24, 0, 4, 23, 137462)),
        ),
    ]
