# Generated by Django 3.1.4 on 2020-12-15 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_auto_20201215_1235'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlackList',
            new_name='BlackListUsers',
        ),
    ]
