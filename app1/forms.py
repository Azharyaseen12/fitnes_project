from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import WeightEntry,Recipe

class AddFoodForm(forms.Form):
    recipe = forms.ModelChoiceField(queryset=Recipe.objects.all(), label='Select Recipe')
    recipe_id = forms.IntegerField()
class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class RegistrationForm(UserCreationForm):
    weight = forms.FloatField()
    height = forms.FloatField()
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    activity_level = forms.ChoiceField(choices=CustomUser.ACTIVITY_LEVEL_CHOICES)
    sex_at_birth = forms.ChoiceField(choices=CustomUser.SEX_CHOICES)
    goal_weight = forms.FloatField()
    goal_activity_level = forms.ChoiceField(choices=CustomUser.ACTIVITY_LEVEL_CHOICES[1:])
    workout_intensity = forms.ChoiceField(choices=CustomUser.WORKOUT_INTENSITY_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'weight', 'height', 'birth_date', 'activity_level', 'sex_at_birth', 'goal_weight', 'goal_activity_level', 'workout_intensity']
