# Generated by Django 4.2.7 on 2024-03-16 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0014_towingrequest_istowable'),
    ]

    operations = [
        migrations.CreateModel(
            name='productrequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=60)),
                ('address', models.CharField(max_length=150)),
                ('contact', models.BigIntegerField()),
                ('productid', models.CharField(max_length=80)),
                ('storeid', models.IntegerField(blank=True, null=True)),
                ('totalprice', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
