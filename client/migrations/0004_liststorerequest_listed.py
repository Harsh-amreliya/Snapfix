# Generated by Django 4.2.7 on 2024-02-14 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_liststorerequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='liststorerequest',
            name='listed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]