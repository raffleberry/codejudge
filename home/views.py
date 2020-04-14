from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from django.contrib import messages

from django.contrib.auth import login, authenticate, logout

from .forms import SigninForm, SignupForm

def index(request):
  if request.user.is_authenticated:
    return HttpResponse("This is the homepage.")
  else:
    return redirect('/signin')

def signin(request):
  if request.method == 'POST':
    form = SigninForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      print(username, password)
      user = authenticate(username=username, password=password)
      print(user)
      if user is not None:
        if user.is_active:
          login(request, user)
      else:
        messages.error(request, 'Incorrect username/password, please try again')
        return redirect('/signin')
  else:
    form = SigninForm()
    if request.user.is_authenticated:
      return redirect(index)
  template = loader.get_template('home/signin.html')
  return HttpResponse(template.render({ 'form' : form },request))

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.save()
      print(form)
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=password)
      login(request, user)
      return redirect(index)
  else:
    form = SignupForm()
    if request.user.is_authenticated:
      return redirect(index)
  template = loader.get_template('home/signup.html')
  return HttpResponse(template.render({ 'form' : form }, request))

def signout(request):
  logout(request)
  messages.error(request, "You've successfully Signed Out!")
  return redirect(signin)