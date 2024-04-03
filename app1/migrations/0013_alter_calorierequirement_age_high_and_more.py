# Generated by Django 4.2.6 on 2024-04-03 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_delete_dailycalorierequirement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calorierequirement',
            name='age_high',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='calorierequirement',
            name='age_low',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='calorierequirement',
            name='female_high_activity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='calorierequirement',
            name='female_low_activity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='calorierequirement',
            name='female_moderate_activity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='calorierequirement',
            name='male_high_activity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='calorierequirement',
            name='male_low_activity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='calorierequirement',
            name='male_moderate_activity',
            field=models.IntegerField(null=True),
        ),
    ]
