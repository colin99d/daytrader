# Generated by Django 3.2.5 on 2021-07-04 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0010_algorithm_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='exchange',
            field=models.CharField(default='NASDAQ', max_length=50),
            preserve_default=False,
        ),
    ]