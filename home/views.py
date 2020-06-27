from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader

from django.contrib import messages

from django.contrib.auth import login, authenticate, logout

from .forms import SigninForm, SignupForm

from .models import Session, Question, Submission

from datetime import datetime

import pytz

from .helpers import *

from .coderunner.question_handler import question as q_run

from django.contrib.auth.models import User

import requests

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
      payload.append({"name" : question["name"], "id" : str(question["id"])})
    
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


def submit(request, sid, qid):
  if not request.user.is_authenticated:
    return JsonResponse({"Error" : "Unauthorized request"})
  else:
    # code, lang,
    post_data = dict(request.POST)

    q_db = Question.objects.get(id=qid)
    s_db = Session.objects.get(id=sid)

    pds = q_db.points_distribution
    pds = pds.split(',')
    pdm = {}
    for pd in pds:
      tmp = pd.split(':')
      pdm[tmp[0]] = int(tmp[1])

    result = q_run(request.POST['code'], str(qid), pdm)

    user = request.user

    submission = Submission()
    submission.question = q_db
    submission.code = request.POST["code"]
    submission.user = user
    submission.points = result["points"]
    submission.session = s_db

    submission.save()
    
    return JsonResponse(result)


def scoreboard(request, sid):
  if not request.user.is_authenticated:
    return redirect('/signin')
  
  template = loader.get_template('home/scoreboard.html')

  try:
    session = Session.objects.get(id=sid)
    questions = session.selectedQuestions.all()
    scoreboard = []

    for user in session.users.all():
      u_users = {
        "user" : user.username
      }

      u_questions = []
      
      total_points = 0
      total_time = 0
      
      for question in questions:
        
        best_attempt = {
          "time_submitted" : datetime(year=3000, month=1, day=1).timestamp(),
          "points": 0
        }
        

        attempts = Submission.objects.filter(user=user, question=question)
        for attempt in attempts:
          if attempt.points > best_attempt["points"]:
            best_attempt["points"] = attempt.points
            best_attempt["time_submitted"] = attempt.time_submitted.timestamp()
          if attempt.points == best_attempt["points"] and attempt.time_submitted.timestamp() < best_attempt["time_submitted"]:
            best_attempt["points"] = attempt.points
            best_attempt["time_submitted"] = attempt.time_submitted.timestamp()
        
        u_attempt = {
          "qid" : question.id,
          "attempt_count" : len(attempts),
          "best_attempt" : best_attempt
        }

        u_questions.append(u_attempt)

        total_points += best_attempt["points"]
        total_time += best_attempt["time_submitted"]
      
      u_users["questions"] = u_questions
      u_users["total_points"] = total_points
      u_users["total_time"] = total_time

      scoreboard.append(u_users)
    
    for i in range(len(scoreboard)):
      for j in range(i+1, len(scoreboard)):
        if (scoreboard[i]["total_points"] < scoreboard[j]["total_points"]):
          scoreboard[i], scoreboard[j] = scoreboard[j], scoreboard[i]
        if (scoreboard[i]["total_points"] == scoreboard[j]["total_points"]):
          if (scoreboard[i]["total_time"] > scoreboard[j]["total_time"]):
            scoreboard[i], scoreboard[j] = scoreboard[j], scoreboard[i]


    for i in range(len(scoreboard)):
      scoreboard[i]["sl"] = str(i + 1)

  except:
    return JsonResponse({"OK" : "No submissions have been made"})
  # return JsonResponse({ 'data' : scoreboard, "username" : request.user.username })
  return HttpResponse(template.render({ 'data' : scoreboard, "username" : request.user.username }, request))