# Generated by Django 3.0.7 on 2020-08-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0003_event_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='body',
            field=models.TextField(max_length=10000),
        ),
    ]
