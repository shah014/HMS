from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

USER_CHOICES = (
    ('D', 'doctor'),
    ('P', 'patient')
)


class CreateUserForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.Select)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        # exclude = ['user']


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        # exclude = ['profile_pic']


class PatientViewForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['email', 'contact', 'age']


class DoctorViewForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['email', 'contact', 'address']


class AppointForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
  

class AvailableBed(ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'
