from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django import forms

numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')

class Question(models.Model):
  name = models.CharField(max_length=100, default="old")
  statement = models.TextField(max_length=20000)
  points_distribution = models.CharField(max_length=100)
  # parse string and check folder for the datasets inputs

  def __str__(self):
    return self.name

class Session(models.Model):
  name = models.CharField(max_length=50)
  users = models.ForeignKey(User, on_delete=models.CASCADE)
  selectedQuestions = models.ManyToManyField(Question)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()

  def __str__(self):
    return self.name

class Submission(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  code = models.TextField(max_length=64000)
  points = models.IntegerField()
  session = models.ForeignKey(Session, on_delete=models.CASCADE)
  
  time_submitted = models.TimeField(auto_now=True)

  def __str__(self):
    return self.question.name + " by " + self.user.get_username()
