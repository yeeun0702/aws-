# Generated by Django 4.0.4 on 2022-07-29 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_num',
            field=models.CharField(default='', max_length=40, null=True),
        ),
    ]
