# Generated by Django 3.2.4 on 2021-06-27 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]