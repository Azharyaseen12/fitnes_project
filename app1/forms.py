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
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date', 'class': 'form-control text-center'}),
            'weight': forms.TextInput(attrs={'placeholder': 'Weight', 'class': 'form-control text-center'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove labels for fields
        self.fields['date'].label = ''
        self.fields['weight'].label = ''

class RegistrationForm(UserCreationForm):
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight'}))
    height = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Birth Date'}))
    activity_level = forms.ChoiceField(choices=CustomUser.ACTIVITY_LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    sex_at_birth = forms.ChoiceField(choices=CustomUser.SEX_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    goal_weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Goal Weight'}))
    goal_activity_level = forms.ChoiceField(choices=CustomUser.ACTIVITY_LEVEL_CHOICES[1:], widget=forms.Select(attrs={'class': 'form-control'}))
    workout_intensity = forms.ChoiceField(choices=CustomUser.WORKOUT_INTENSITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'weight', 'height', 'birth_date', 'activity_level', 'sex_at_birth', 'goal_weight', 'goal_activity_level', 'workout_intensity']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})