# Generated by Django 4.2.7 on 2024-03-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_towingrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='towingrequest',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='towingrequest',
            name='serviceid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='towingrequest',
            name='storeid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
