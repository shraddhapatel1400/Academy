# Generated by Django 3.1 on 2020-09-07 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20200905_1406'),
        ('lecture', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Student',
            new_name='Lecture',
        ),
    ]