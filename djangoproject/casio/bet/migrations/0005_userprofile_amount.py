# Generated by Django 4.0 on 2023-02-19 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0004_userprofile_city_userprofile_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='amount',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
