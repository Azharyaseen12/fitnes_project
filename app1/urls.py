from django.urls import path
from .views import detail_exercise, register,user_login,generate_user_workout,view_workout,add_exercise,remove_exercise

urlpatterns = [
    path('',register , name = 'register' ),
    path('login/', user_login, name='login'),
    path('generate_user_workout/', generate_user_workout, name='generate_user_workout'),
    path('view_workout/', view_workout, name='view_workout'),
    path('add_exercise/', add_exercise, name='add_exercise'),
    path('remove_exercise/<int:workout_id>', remove_exercise, name='remove_exercise'),
    path('detail_exercise/<str:exercise>/', detail_exercise, name='detail_exercise'),
]