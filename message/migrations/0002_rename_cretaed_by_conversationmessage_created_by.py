# Generated by Django 4.1.2 on 2023-09-08 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversationmessage',
            old_name='cretaed_by',
            new_name='created_by',
        ),
    ]