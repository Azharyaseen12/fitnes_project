import random
import os
import csv
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,WeightEntryForm,AddFoodForm
from .models import CustomUser, Exercise, Workout,Recipe,CalorieRequirement,DietPlan,WeightEntry
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib.auth import logout
from datetime import date,timedelta
# registration
def home(request):
    return render(request, 'base.html')
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
                return redirect('generate_user_workout')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Workout
@login_required(login_url='login')
def generate_user_workout(request):
    user = request.user
    activity_level = user.activity_level
    goal_activity_level = user.goal_activity_level
    workout_plan = generate_workout_plan(activity_level, goal_activity_level)
    store_workout_plan(user, workout_plan)
    return redirect('view_workout')


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
@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def remove_exercise(request, workout_id):
    workout = Workout.objects.get(pk=workout_id)
    workout.delete()
    return redirect('view_workout')
@login_required(login_url='login')
def detail_exercise(request, exercise):
    details = Exercise.objects.filter(name=exercise).first()
    # print(details.exercise_type)
    return render(request, 'detail_exercise.html', {'exercise': details})

def import_recipe_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row.get('title')
            calories = row.get('calories', None)
            protein = row.get('protein', None)
            fat = row.get('fat', None)

            if calories == '':
                calories = 0.0
            else:
                calories = float(calories)
            if protein == '':
                protein = 0.0
            else:
                protein = float(protein)
            if fat == '':
                fat = 0.0
            else:
                fat = float(fat)
            # Create Recipe instance
            recipe = Recipe.objects.create(
                title=title,
                calories=calories,
                protein=protein,
                fat=fat
            )
            recipe.save()

# Usage example
file_path = os.path.join('F:\\', 'falconxoft internship', 'project4', 'csv_files', 'recepies.csv')  # Corrected file name
# import_recipe_from_csv(file_path)
def import_calorie_requirements_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            calorie_req = CalorieRequirement.objects.create(
                age_low=row.get('age_low'),  # Change column names accordingly
                age_high=row.get('age_high'),
                male_low_activity=row.get('male_low_activity'),
                male_moderate_activity=row.get('male_moderate_activity'),
                male_high_activity=row.get('male_high_activity'),
                female_low_activity=row.get('female_low_activity'),
                female_moderate_activity=row.get('female_moderate_activity'),
                female_high_activity=row.get('female_high_activity')
            )
            calorie_req.save()

file_path = os.path.join('F:\\', 'falconxoft internship', 'project4', 'csv_files', 'calories.csv')  # Corrected file name
# import_calorie_requirements_from_csv(file_path)


# weight tracker work start

def add_weight_entry(user, weight, date):
    WeightEntry.objects.create(user=user, weight=weight, date=date)
@login_required(login_url='login')
def add_weight(request):
    if request.method == 'POST':
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            weight_entry = form.save(commit=False)
            weight_entry.user = request.user 
            weight_entry.save()
            return redirect('weight_tracker')
    else:
        form = WeightEntryForm()
    return render(request, 'add_weight.html', {'form': form})

@login_required(login_url='login')
def weight_tracker(request):
    weight_entries = WeightEntry.objects.filter(user=request.user).order_by('date')
    dates = [entry.date for entry in weight_entries]
    weights = [entry.weight for entry in weight_entries]

    # Generate the graph
    plt.figure(figsize=(10, 6))
    plt.plot(dates, weights, marker='o', linestyle='-', color='b')
    plt.title('Weight Tracker')
    plt.xlabel('Date')
    plt.ylabel('Weight (kg)')
    plt.xticks(rotation=45)
    
    # Convert plot to bytes and embed in HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return render(request, 'weight_tracker.html', {'graph': graph})

# def get_weight_data(user):
#     weight_entries = WeightEntry.objects.filter(user=user).order_by('date')
#     dates = [entry.date for entry in weight_entries]
#     weights = [entry.weight for entry in weight_entries]
#     return dates, weights



@login_required(login_url='login')
def calculate_daily_calorie_goal(sex, age, activity_level):
    try:
        calorie_requirement = CalorieRequirement.objects.filter(
            age_low__lte=age,
            age_high__gte=age
        ).first()

        if sex == 'male':
            if activity_level == 'low':
                return calorie_requirement.male_low_activity
            elif activity_level == 'moderate':
                return calorie_requirement.male_moderate_activity
            elif activity_level == 'high':
                return calorie_requirement.male_high_activity
        elif sex == 'female':
            if activity_level == 'low':
                return calorie_requirement.female_low_activity
            elif activity_level == 'moderate':
                return calorie_requirement.female_moderate_activity
            elif activity_level == 'high':
                return calorie_requirement.female_high_activity
    except CalorieRequirement.DoesNotExist:
        return None

def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

@login_required(login_url='login')
def generate_diet_plan(request):
    # Assuming you have access to the user's sex, age, and activity level
    user = request.user
    # print(user.sex_at_birth)
    sex = user.sex_at_birth
    age = calculate_age(user.birth_date)
    activity_level = user.activity_level

    daily_calorie_goal = calculate_daily_calorie_goal(sex, age, activity_level)
    daily_calorie_range = daily_calorie_goal  

    existing_diet_plans = DietPlan.objects.filter(user=user)
    if existing_diet_plans.exists():
        # If a diet plan already exists for the user, return the existing plan
        # return render(request, 'diet_plan.html', {'diet_plans': existing_diet_plans})
        return render(request, 'diet_plan.html', {'diet_plans': existing_diet_plans ,'daily_calorie_goal': daily_calorie_goal})
    else:
        diet_plan = {}
        start_date = datetime.datetime.now().date()
        for day in range(28):
            target_calories = daily_calorie_goal - (daily_calorie_range / 2) + (daily_calorie_range * random.random())
            recipes = Recipe.objects.filter(calories__gte=target_calories - (daily_calorie_range / 2),
                                            calories__lte=target_calories + (daily_calorie_range / 2))
            selected_recipe = random.choice(recipes)
            diet_plan[start_date + timedelta(days=day)] = selected_recipe
    
        diet_plan_instance = DietPlan(user=user,date=start_date)
        diet_plan_instance.save()
        for date, recipe in diet_plan.items():
            diet_plan_instance.recipes.add(recipe, through_defaults={'date': date})

        diet_plans = DietPlan.objects.filter(user=user)
        return render(request, 'diet_plan.html', {'diet_plans': diet_plans ,'daily_calorie_goal': daily_calorie_goal})


@login_required(login_url='login')
def add_food_to_diet_plan(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        try:
                recipe = Recipe.objects.get(pk=recipe_id)
                diet_plan, _ = DietPlan.objects.get_or_create(user=request.user)
                diet_plan.recipes.add(recipe)
                return HttpResponse('success_page')  # Redirect to success page or any other page
        except Recipe.DoesNotExist:
                # Handle case where recipe with given ID does not exist
                return render(request, 'error.html', {'message': 'Recipe not found'})
    else:
        recipe = Recipe.objects.all()
    return render(request, 'add_food_to_diet_plan.html', {'recipe':recipe})
@login_required(login_url='login')
def remove_food(request,id):
    if request.method == 'GET':
        recipe = Recipe.objects.filter(pk=id).first()
        diet_plan, _ = DietPlan.objects.get_or_create(user=request.user)
        diet_plan.recipes.remove(recipe)
        return HttpResponse('recipe deleted')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    # Redirect to a specific URL after logout, or to the homepage
    return redirect('login') 