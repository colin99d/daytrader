# Generated by Django 3.2.5 on 2021-07-08 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0018_alter_stock_listed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='listed',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
