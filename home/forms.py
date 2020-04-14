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

# class SignupForm(forms.Form):
#   first_name = forms.CharField(
#     min_length=2,
#     label = "FirstName",
#     required=True,
#     widget = forms.TextInput(
#       attrs = {
#         "placeholder" : "First Name"
#       }
#     )
#   )
#   last_name = forms.CharField(
#     min_length=2,
#     label = "LastName",
#     required=True,
#     widget = forms.TextInput(
#       attrs = {
#         "placeholder" : "Last Name"
#       }
#     )
#   )
#   roll = forms.CharField(
#     min_length = 4,
#     max_length=10,
#     label = "RollNo",
#     widget = forms.NumberInput(
#       attrs = {
#         "placeholder" : "Roll No."
#       }
#     ),
#     required = True
#   )
#   email = forms.EmailField(
#     required=True,
#     widget = forms.EmailInput(
#       attrs = {
#         "placeholder" : "Email"
#       }
#     )
#   )
#   password = forms.CharField(
#     min_length=8,
#     widget=forms.PasswordInput(
#       attrs = {
#         "placeholder" : "Password"
#       }
#     ),
#     required=True
#   )
#   confirm_password = forms.CharField(
#     min_length=8,
#     widget=forms.PasswordInput(
#       attrs = {
#         "placeholder" : "Confirm Password"
#       }
#     ),
#     required=True,
#   )

#   def clean(self):
#     cleaned_data = super(SignupForm, self).clean()
#     password = cleaned_data.get('password')
#     confirm_password = cleaned_data.get('confirm_password')

#     if password != confirm_password:
#       raise forms.ValidationError({ "confirm_password" : ["Passwords must match"], "password" : ["Passwords must match"] })
#     return cleaned_data
  
#   class Meta:
#     model = Student
#     fields = ('first_name', 'last_name', 'roll', 'password', 'confirm_password')