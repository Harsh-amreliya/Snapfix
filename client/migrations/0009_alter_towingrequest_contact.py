# Generated by Django 4.2.7 on 2024-03-05 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_towingrequest_quantity_towingrequest_serviceid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='towingrequest',
            name='contact',
            field=models.BigIntegerField(),
        ),
    ]