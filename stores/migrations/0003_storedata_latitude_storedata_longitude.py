# Generated by Django 4.2.7 on 2024-01-31 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_alter_storedata_closingtime_alter_storedata_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storedata',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='storedata',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
