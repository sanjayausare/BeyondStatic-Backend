# Generated by Django 3.2.3 on 2021-05-20 14:38

import datetime
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
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('endpointURL', models.CharField(max_length=14000)),
                ('field1Name', models.CharField(default=' ', max_length=50)),
                ('field2Name', models.CharField(default=' ', max_length=50)),
                ('field3Name', models.CharField(default=' ', max_length=50)),
                ('field4Name', models.CharField(default=' ', max_length=50)),
                ('field5Name', models.CharField(default=' ', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field1', models.CharField(default=' ', max_length=10000000)),
                ('field2', models.CharField(default=' ', max_length=10000000)),
                ('field3', models.CharField(default=' ', max_length=10000000)),
                ('field4', models.CharField(default=' ', max_length=10000000)),
                ('field5', models.CharField(default=' ', max_length=10000000)),
                ('dateTime', models.DateTimeField(default=datetime.datetime(2021, 5, 20, 20, 8, 7, 188062))),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='brooklyn.project')),
            ],
        ),
    ]