from django.contrib import admin
from .models import CustomUser,Workout,Exercise,CalorieRequirement,Recipe,DietPlan,WeightEntry
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(CalorieRequirement)
admin.site.register(Recipe)
admin.site.register(DietPlan)
admin.site.register(WeightEntry)