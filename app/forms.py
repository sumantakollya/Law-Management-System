from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class ClientForm(ModelForm):
	class Meta:
		model = Client
		fields = '__all__'
		exclude = ['user']

class LawyerForm(ModelForm):
	class Meta:
		model = Lawyer
		fields = '__all__'
		exclude = ['user']

class LegalServiceForm(ModelForm):
	class Meta:
		model = LegalService
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	is_lawyer = forms.BooleanField()
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']