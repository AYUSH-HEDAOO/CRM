from django.forms import ModelForm
from .models import Customer, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'

class createUserForm(UserCreationForm):
	class meta:
		model=User
		fields=['username','email','password1','password2']
		