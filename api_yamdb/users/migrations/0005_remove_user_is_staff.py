# Generated by Django 2.2.16 on 2022-10-11 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_is_moderator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
