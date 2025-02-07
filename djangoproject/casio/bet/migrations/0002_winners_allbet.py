# Generated by Django 4.0 on 2023-02-17 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='winners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bet', models.CharField(max_length=10)),
                ('win', models.BooleanField()),
                ('number', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bet.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Allbet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number1', models.IntegerField(max_length=2)),
                ('number2', models.IntegerField(max_length=2)),
                ('number3', models.IntegerField(max_length=2)),
                ('number4', models.IntegerField(max_length=2)),
                ('number5', models.IntegerField(max_length=2)),
                ('totalpot', models.IntegerField(max_length=100)),
                ('winning_one', models.IntegerField(max_length=2)),
                ('winning_two', models.IntegerField(max_length=2)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('closed', models.BooleanField(default=False)),
                ('winners', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bet.winners')),
            ],
        ),
    ]
