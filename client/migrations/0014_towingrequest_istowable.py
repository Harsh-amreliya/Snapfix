# Generated by Django 4.2.7 on 2024-03-15 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0013_alter_towingrequest_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='towingrequest',
            name='istowable',
            field=models.BooleanField(blank=True, default=0, null=True),
        ),
    ]
