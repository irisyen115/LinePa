# Generated by Django 4.0.6 on 2022-08-16 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_music_song'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['-id']},
        ),
    ]
