# Generated by Django 4.1.2 on 2023-09-07 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0002_alter_category_options_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='point',
            field=models.IntegerField(),
        ),
    ]
