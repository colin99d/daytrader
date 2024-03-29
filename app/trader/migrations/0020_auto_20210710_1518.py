# Generated by Django 3.2.5 on 2021-07-10 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0019_alter_stock_listed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='decision',
            name='openPrice',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
