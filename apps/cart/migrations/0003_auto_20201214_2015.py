# Generated by Django 3.1.4 on 2020-12-14 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_purchaseshistory_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseshistory',
            options={'verbose_name': 'История покупок', 'verbose_name_plural': 'История покупок'},
        ),
    ]
