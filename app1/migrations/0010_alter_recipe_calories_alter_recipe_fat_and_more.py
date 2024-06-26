# Generated by Django 4.2.6 on 2024-04-03 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_alter_recipe_fat_alter_recipe_protein'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='calories',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='fat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='protein',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
