# Generated by Django 3.2.13 on 2022-06-29 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='music',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='music',
            old_name='song',
            new_name='song_name',
        ),
        migrations.RenameField(
            model_name='music',
            old_name='last_modify_date',
            new_name='updated_at',
        ),
        migrations.RemoveField(
            model_name='music',
            name='singer',
        ),
        migrations.AddField(
            model_name='music',
            name='song_num',
            field=models.TextField(default='32410'),
        ),
    ]