# Generated by Django 4.2.7 on 2024-04-02 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('servicestore', '0007_servicelisting_towable'),
    ]

    operations = [
        migrations.CreateModel(
            name='servicelisting2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('towable', models.BooleanField(default=0)),
                ('avgtime', models.CharField(max_length=60)),
                ('servicename', models.CharField(max_length=80)),
                ('serviceimage', models.FileField(upload_to='servicestoredata/service_image/')),
                ('serviceprice', models.IntegerField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicestore.servicestoredata')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
