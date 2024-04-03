from .models import Workout
import random


def generate_workout(activity_level, goal_activity_level):
    workout_plan = []

    # Determine the number of days and exercises per week based on activity level and goal activity level
    if goal_activity_level == 'light':
        days_per_week = 1
    elif goal_activity_level == 'moderate':
        days_per_week = 2
    elif goal_activity_level == 'intense':
        days_per_week = 4
    elif goal_activity_level == 'top_athlete':
        days_per_week = 6

    # Generate workout plan for each week
    for week_number in range(1, 5):
        for day_number in range(1, 8):
            exercise = f"Exercise {day_number}"
            Workout.objects.create(user=request.user, week_number=week_number, day_number=day_number, exercise=exercise)

    for week_number in range(1, 5):
        for day_number in range(1, days_per_week + 1):
            # Generate random exercises based on workout intensity
            if activity_level == 'light':
                exercises_per_day = 2
            elif activity_level == 'moderate':
                exercises_per_day = 4
            elif activity_level == 'intense':
                exercises_per_day = 8
            
            # Add warmup exercise at the beginning of each day
            workout_plan.append({'week_number': week_number, 'day_number': day_number, 'exercise': 'Warmup'})

            for _ in range(exercises_per_day - 1):  # Subtract 1 for warmup exercise
                # Randomly select an exercise from the database
                exercise = random.choice(Workout.objects.all())
                workout_plan.append({'week_number': week_number, 'day_number': day_number, 'exercise': exercise.name})

    return workout_plan
