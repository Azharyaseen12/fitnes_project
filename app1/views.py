import random
import os
import csv
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import CustomUser, Exercise, Workout,Recipe
import datetime
from collections import defaultdict

# registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('generate_user_workout')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('view_workout')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



# Workout
@login_required
def generate_user_workout(request):
    user = request.user
    activity_level = user.activity_level
    goal_activity_level = user.goal_activity_level
    workout_plan = generate_workout_plan(activity_level, goal_activity_level)
    store_workout_plan(user, workout_plan)
    return HttpResponse('Workout plan generated and stored successfully.')


def generate_workout_plan(activity_level, goal_activity_level):
    workout_plan = []

    for week_number in range(1, 5):
        if week_number < 3:
            num_days = get_num_days(activity_level)
        else:
            num_days = get_num_days(goal_activity_level)

        for day_number in range(1, num_days + 1):
            exercises_per_day = get_exercises_per_day(activity_level)

            # Add warmup exercise at the beginning of each day
            workout_plan.append({'week_number': week_number, 'day_number': day_number, 'exercise': 'Warmup'})

            for _ in range(exercises_per_day):
                exercise = select_random_exercise(activity_level)
                workout_plan.append({'week_number': week_number, 'day_number': day_number, 'exercise': exercise})

    return workout_plan


def get_num_days(activity_level):
    if activity_level == 'sedentary':
        return 1
    elif activity_level == 'light':
        return 1
    elif activity_level == 'moderate':
        return 2
    elif activity_level == 'intense':
        return 4
    elif activity_level == 'top_athlete':
        return 6


def get_exercises_per_day(activity_level):
    if activity_level == 'light':
        return 2
    elif activity_level == 'moderate':
        return 4
    elif activity_level == 'intense':
        return 8


def select_random_exercise(activity_level):
    if activity_level == 'light':
        exercises = Exercise.objects.filter(beginner=True)
    elif activity_level == 'moderate':
        exercises = Exercise.objects.filter(intermediate=True)
    elif activity_level == 'intense':
        exercises = Exercise.objects.filter(intermediate=True) | Exercise.objects.filter(advanced=True)

    return random.choice(exercises).name


def store_workout_plan(user, workout_plan):
    for workout in workout_plan:
        Workout.objects.create(user=user, **workout)





def import_exercises_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            exercise = Exercise.objects.create(
                name=row['Exercise'],
                exercise_type=row['Exercise Type'],
                movement_type=row['Movement Type'],
                muscle_group=row['Muscle Group'],
                major_muscle=row['Major Muscle'],
                minor_muscle=row['Minor Muscle'],
                notes=row['Notes'],
                modifications=row['Modifications'],
                beginner=row['Beginner'],
                intermediate=row['Intermediate'],
                advanced=row['Advanced'],
                warmup=row['Warmup']
            )

# Usage example
file_path = os.path.join('F:\\', 'falconxoft internship', 'project4', 'csv_files', 'exercises_raw.csv')
# import_exercises_from_csv(file_path)



# now display the workouts
@login_required
def view_workout(request):
    # Retrieve workouts for the user
    workouts = Workout.objects.filter(user=request.user).order_by('week_number', 'day_number')

    # Organize workouts by day
    workout_plan = defaultdict(list)
    for workout in workouts:
        workout_plan[(workout.week_number, workout.day_number)].append(workout)

    # Convert defaultdict to a list of dictionaries
    workout_plan_list = []
    for day, workouts in workout_plan.items():
        week_number, day_number = day
        workout_plan_list.append({
            'week_number': week_number,
            'day_number': day_number,
            'workouts': workouts
        })

    return render(request, 'view_workout.html', {'workout_plan': workout_plan_list})
# def view_workout(request):
#     user = request.user
#     workout = Workout.objects.filter(user=user)
#     return render(request, 'view_workout.html', {'workout': workout})

@login_required
def add_exercise(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        week_number = request.POST.get('week_number')
        day = request.POST.get('day')
        exercise = Exercise.objects.get(pk=exercise_id)
        user = request.user
        Workout.objects.create(user=user, exercise=exercise.name,week_number=week_number,day_number=day)
        return redirect('view_workout')
    else:
        exercises = Exercise.objects.all()
        return render(request, 'add_excercise.html', {'exercises': exercises})

@login_required
def remove_exercise(request, workout_id):
    workout = Workout.objects.get(pk=workout_id)
    workout.delete()
    return redirect('view_workout')
@login_required
def detail_exercise(request, exercise):
    details = Exercise.objects.filter(name=exercise).first()
    # print(details.exercise_type)
    return render(request, 'detail_exercise.html', {'exercise': details})


# def import_recipe_from_csv(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             title = row['title']
#             rating = row.get('rating', None)
#             calories = row.get('calories', None)
#             protein = row.get('protein', None)
#             fat = row.get('fat', None)

#             # Create Recipe instance
#             recipe = Recipe.objects.create(
#                 title=title,
#                 rating=rating,
#                 calories=calories,
#                 protein=protein,
#                 fat=fat
#             )
#             recipe.save()

# # Usage example
# file_path = os.path.join('F:\\', 'falconxoft internship', 'project4', 'csv_files', 'recipes.csv')
# import_recipe_from_csv(file_path)