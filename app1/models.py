from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime 


class CustomUser(AbstractUser):
    weight = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    birth_date = models.DateField(default=datetime.date.today)
    ACTIVITY_LEVEL_CHOICES = [
        # ('sedentary', 'Sedentary - No activity'),
        ('light', 'Light activity - Once a week'),
        ('moderate', 'Moderate activity - 2/3 times a week'),
        ('intense', 'Intense activity - 4/5 days a week'),
        ('top_athlete', 'Top athlete - Every day'),
    ]
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    sex_at_birth = models.CharField(max_length=10, choices=SEX_CHOICES)
    goal_weight = models.FloatField(default=0.0)
    goal_activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES[1:])
    WORKOUT_INTENSITY_CHOICES = [
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('intense', 'Intense'),
    ]
    workout_intensity = models.CharField(max_length=10, choices=WORKOUT_INTENSITY_CHOICES)

    # Specify related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        )
    
class Workout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    week_number = models.IntegerField()
    day_number = models.IntegerField()
    exercise = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    exercise_type = models.CharField(max_length=50)
    movement_type = models.CharField(max_length=50)
    muscle_group = models.CharField(max_length=50)
    major_muscle = models.CharField(max_length=50)
    minor_muscle = models.CharField(max_length=50)
    notes = models.TextField()
    modifications = models.TextField()
    beginner = models.BooleanField()
    intermediate = models.BooleanField()
    advanced = models.BooleanField()
    warmup = models.BooleanField()

    def __str__(self):
        return self.name

class CalorieRequirement(models.Model):
    age_low = models.IntegerField(null=True)
    age_high = models.IntegerField(null=True)
    male_low_activity = models.IntegerField(null=True)
    male_moderate_activity = models.IntegerField(null=True)
    male_high_activity = models.IntegerField(null=True)
    female_low_activity = models.IntegerField(null=True)
    female_moderate_activity = models.IntegerField(null=True)
    female_high_activity = models.IntegerField(null=True)


# class DailyCalorieRequirement(models.Model):
#     sex = models.CharField(max_length=10)
#     age = models.IntegerField()
#     activity_level = models.CharField(max_length=10)
#     calorie_goal = models.IntegerField()

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    calories = models.FloatField(null=True)
    protein = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.title
    
class DietPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return f"Diet Plan for {self.user.username} on {self.date}"

class WeightEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Assuming weight is stored in kilograms
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s Weight Entry on {self.date}"