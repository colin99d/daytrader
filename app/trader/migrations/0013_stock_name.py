# Generated by Django 3.2.5 on 2021-07-05 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0012_stock_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]