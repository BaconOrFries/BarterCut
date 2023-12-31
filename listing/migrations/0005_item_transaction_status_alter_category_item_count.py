# Generated by Django 4.1.2 on 2023-09-08 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0004_category_item_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='transaction_status',
            field=models.CharField(choices=[('Listed', 'Listed'), ('Sold', 'Sold'), ('Received', 'Received')], default='Listed', max_length=10),
        ),
        migrations.AlterField(
            model_name='category',
            name='item_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
