# Generated by Django 5.1.3 on 2024-12-15 07:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('store_name', models.CharField(max_length=25)),
                ('store_num', models.IntegerField(primary_key=True, serialize=False)),
                ('store_email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', models.IntegerField()),
                ('average_sale', models.FloatField()),
                ('door_count', models.IntegerField()),
                ('date_entered', models.DateField(auto_now_add=True)),
                ('datetime_entered', models.TimeField(auto_now_add=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SalesEntrySite.store')),
            ],
        ),
        migrations.CreateModel(
            name='DailyBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('budget', models.IntegerField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SalesEntrySite.store')),
            ],
        ),
    ]
