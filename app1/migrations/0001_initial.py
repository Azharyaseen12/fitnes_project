# Generated by Django 4.2.6 on 2024-04-01 12:34

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('weight', models.FloatField()),
                ('height', models.FloatField()),
                ('birth_date', models.DateField()),
                ('activity_level', models.CharField(choices=[('sedentary', 'Sedentary - No activity'), ('light', 'Light activity - Once a week'), ('moderate', 'Moderate activity - 2/3 times a week'), ('intense', 'Intense activity - 4/5 days a week'), ('top_athlete', 'Top athlete - Every day')], max_length=20)),
                ('sex_at_birth', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('goal_weight', models.FloatField()),
                ('goal_activity_level', models.CharField(choices=[('light', 'Light activity - Once a week'), ('moderate', 'Moderate activity - 2/3 times a week'), ('intense', 'Intense activity - 4/5 days a week'), ('top_athlete', 'Top athlete - Every day')], max_length=20)),
                ('workout_intensity', models.CharField(choices=[('light', 'Light'), ('medium', 'Medium'), ('intense', 'Intense')], max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='custom_user_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
