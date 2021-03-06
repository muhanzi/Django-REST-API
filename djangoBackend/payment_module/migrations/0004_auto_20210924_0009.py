# Generated by Django 3.1.2 on 2021-09-23 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_module', '0003_auto_20210924_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='commission',
            name='updatedAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='updatedAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='updatedAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='updatedAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
