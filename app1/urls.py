from django.urls import path
from .views import add_food_to_diet_plan,remove_food,detail_exercise,add_weight,generate_diet_plan,weight_tracker, register,user_login,generate_user_workout,view_workout,add_exercise,remove_exercise

urlpatterns = [
    path('',register , name = 'register' ),
    path('login/', user_login, name='login'),
    path('generate_user_workout/', generate_user_workout, name='generate_user_workout'),
    path('view_workout/', view_workout, name='view_workout'),
    path('add_exercise/', add_exercise, name='add_exercise'),
    path('remove_exercise/<int:workout_id>', remove_exercise, name='remove_exercise'),
    path('detail_exercise/<str:exercise>/', detail_exercise, name='detail_exercise'),
    path('add_weight/', add_weight, name='add_weight'),
    path('weight_tracker/', weight_tracker, name='weight_tracker'),
    path('generate_diet_plan/', generate_diet_plan, name='generate_diet_plan'),
    path('add_food_to_diet_plan/', add_food_to_diet_plan, name='add_food_to_diet_plan'),
    path('remove_food/<int:id>/', remove_food, name='remove_food'),
]