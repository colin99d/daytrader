# Generated by Django 3.2.5 on 2021-07-06 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0014_alter_stock_exchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='volume',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]