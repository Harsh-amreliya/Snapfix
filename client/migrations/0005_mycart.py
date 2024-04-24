# Generated by Django 4.2.7 on 2024-02-23 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_productlisting_store'),
        ('servicestore', '0006_servicelisting_store'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0004_liststorerequest_listed'),
    ]

    operations = [
        migrations.CreateModel(
            name='mycart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.productlisting')),
                ('serviceid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicestore.servicelisting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
