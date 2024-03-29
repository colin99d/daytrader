# Generated by Django 3.2.4 on 2021-06-13 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='stock',
            name='ticker',
            field=models.CharField(max_length=5, unique=True),
        ),
        migrations.CreateModel(
            name='DecisionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('algorithm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trader.algorithm')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trader.stock')),
            ],
        ),
    ]
