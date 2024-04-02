# Generated by Django 4.2.6 on 2024-04-02 04:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_customuser_height_alter_customuser_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='goal_weight',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='height',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='weight',
            field=models.FloatField(default=0.0),
        ),
    ]