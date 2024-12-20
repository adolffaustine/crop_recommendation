from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Crop

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class CreateUserForm(UserCreationForm):
   

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DataForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Soil_pH']