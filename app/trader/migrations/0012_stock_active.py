# Generated by Django 3.2.5 on 2021-07-04 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0011_stock_exchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]