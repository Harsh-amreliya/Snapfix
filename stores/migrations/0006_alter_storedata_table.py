# Generated by Django 4.2.7 on 2024-02-26 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_productlisting_store'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='storedata',
            table='stdata',
        ),
    ]
