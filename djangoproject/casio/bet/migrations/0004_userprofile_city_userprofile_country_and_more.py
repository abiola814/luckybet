# Generated by Django 4.0 on 2023-02-18 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0003_remove_allbet_winners_alter_allbet_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(default=12, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(default=12, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='withdraw_pin',
            field=models.CharField(default='er', max_length=100),
            preserve_default=False,
        ),
    ]
