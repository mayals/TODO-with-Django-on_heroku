# Generated by Django 3.2.5 on 2021-08-05 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='T_name',
            field=models.CharField(max_length=15),
        ),
    ]
