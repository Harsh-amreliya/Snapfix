# Generated by Django 4.2.7 on 2024-04-05 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0008_productlisting_active_usecategory_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedata',
            name='hsnsac',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]