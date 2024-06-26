# Generated by Django 4.2.7 on 2024-01-18 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='usecategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=60)),
                ('companyname', models.CharField(max_length=90)),
                ('modelname', models.CharField(max_length=100)),
                ('modelyear', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='storedata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entered_store_details', models.BooleanField(default=False)),
                ('ownername', models.CharField(max_length=70)),
                ('storename', models.CharField(max_length=80)),
                ('storecontact', models.BigIntegerField()),
                ('email', models.EmailField(max_length=80)),
                ('openingtime', models.TimeField()),
                ('closingtime', models.TimeField()),
                ('ownercontact', models.BigIntegerField()),
                ('storeaddress', models.CharField(max_length=180)),
                ('storelicencedocument', models.FileField(blank=True, null=True, upload_to='storedata/licence_doc/')),
                ('ownersdocument', models.FileField(blank=True, null=True, upload_to='storedata/aadhar_doc/')),
                ('imageofstore', models.FileField(blank=True, null=True, upload_to='storedata/store_image/')),
                ('storeestablishment', models.DateField()),
                ('gstno', models.CharField(max_length=15)),
                ('hsnsac', models.IntegerField()),
                ('is_activee', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='productlisting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(max_length=100)),
                ('productimage', models.ImageField(blank=True, null=True, upload_to='storedata/product_image/')),
                ('productprice', models.IntegerField()),
                ('modelyear', models.IntegerField()),
                ('companyname', models.CharField(max_length=80)),
                ('usecategorylist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.usecategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
