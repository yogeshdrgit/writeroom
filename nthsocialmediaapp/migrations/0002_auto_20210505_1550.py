# Generated by Django 3.1.7 on 2021-05-05 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nthsocialmediaapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='auther',
            new_name='author',
        ),
    ]
