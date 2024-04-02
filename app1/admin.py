from django.contrib import admin
from .models import CustomUser,Workout,Exercise,DailyCalorieRequirement,Recipe
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(DailyCalorieRequirement)
admin.site.register(Recipe)