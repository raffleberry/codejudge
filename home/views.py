from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from django.contrib import messages

from django.contrib.auth import login, authenticate, logout

from .forms import SigninForm, SignupForm

from .models import Session, Question

from datetime import datetime

import pytz

from .helpers import *

def index(request):
  if not request.user.is_authenticated:
    return redirect('/signin')
  else:
    template = loader.get_template('home/index.html')
    sessions = Session.objects.all()
    
    table = []

    now = datetime.now(tz=pytz.UTC)

    for i in range(len(sessions)):
      table.append({
        'name' : sessions[i].name,
        'id' : sessions[i].id,
        'status_text' : '',
        'status_code' : '',
        'time' : ''
      })

      table[i].update(status(sessions[i].start_time, sessions[i].end_time, now))

    data = {
      'username' : request.user.username,
      'table' : table
    }

    return HttpResponse(template.render({ 'data' : data }, request))

def signin(request):
  if request.method == 'POST':
    form = SigninForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect(index)
      else:
        messages.error(request, 'Incorrect username/password, please try again')
        return redirect('/signin')
  else:
    form = SigninForm()
    if request.user.is_authenticated:
      return redirect(index)
  template = loader.get_template('home/signin.html')
  return HttpResponse(template.render({ 'form' : form }, request))

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.save()
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


def session(request, sid):
  if not request.user.is_authenticated:
    return redirect('/signin')
  else:
    template = loader.get_template('home/session.html')
    session = Session.objects.get(id=sid)
    questions = list(session.selectedQuestions.values())
    payload = []
    for question in questions:
      payload.append({"name" : question["name"], "id" : str(sid) + "/" + str(question["id"])})
    
    now = datetime.now(tz=pytz.UTC)

    data = {
      "questions" : payload,
      "username" : request.user.username,
      "status" : status(session.start_time, session.end_time, now)
    }
    
    return HttpResponse(template.render({ 'data' : data }, request))


def question(request, sid, qid):
  if not request.user.is_authenticated:
    return redirect('/signin')
  else:
    template = loader.get_template('home/question.html')
    question = Question.objects.get(id=qid)
    


    data = {
      "username" : request.user.username,
      "name" : question.name,
      "statement": question.statement,
    }
    return HttpResponse(template.render({ 'data' : data }, request))

