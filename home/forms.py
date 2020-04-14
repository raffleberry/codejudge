from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SigninForm(forms.Form):
  username = forms.CharField(
    min_length = 4,
    label = "Username",
    widget = forms.TextInput(
      attrs = {
        "placeholder" : "Username"
      }
    ),
    required = True
  )
  password = forms.CharField(
    min_length=8,
    label = "Password",
    widget = forms.PasswordInput(
      attrs = {
        "placeholder" : "Password"
      }
    ),
    required = True
  )

class SignupForm(UserCreationForm):
  first_name = forms.CharField(
    min_length=2,
    max_length=30,
    label = "FirstName",
    required=True,
    widget = forms.TextInput(
      attrs = {
        "placeholder" : "First Name"
      }
    )
  )
  last_name = forms.CharField(
    min_length=2,
    max_length=30,
    label = "LastName",
    required=True,
    widget = forms.TextInput(
      attrs = {
        "placeholder" : "Last Name"
      }
    )
  )
  email = forms.EmailField(
    max_length = 254,
    required=True,
    widget = forms.EmailInput(
      attrs = {
        "placeholder" : "Email"
      }
    )
  )
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')