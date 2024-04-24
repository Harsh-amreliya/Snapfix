# Generated by Django 4.2.7 on 2024-02-23 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_productlisting_store'),
        ('servicestore', '0006_servicelisting_store'),
        ('client', '0005_mycart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycart',
            name='productid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.productlisting'),
        ),
        migrations.AlterField(
            model_name='mycart',
            name='serviceid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servicestore.servicelisting'),
        ),
    ]