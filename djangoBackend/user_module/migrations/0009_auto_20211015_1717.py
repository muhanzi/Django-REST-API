# Generated by Django 3.1.2 on 2021-10-15 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_module', '0008_auto_20211010_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='bioData',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='dateOfBirth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='lc1Name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='parentGuardian',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='profilePicture',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='village',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='bankAccountNumber',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='bankName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='dateOfBirth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='nin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='profilePicture',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recrutingagency',
            name='village',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='supersite',
            name='profilePicture',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
