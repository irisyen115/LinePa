# Generated by Django 4.0.6 on 2022-08-16 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='keyword',
            field=models.TextField(default=''),
        ),
    ]
