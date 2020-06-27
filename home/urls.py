from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('<int:sid>/', views.session, name='session'),
    path('<int:sid>/<int:qid>/', views.question, name='question'),
    path('<int:sid>/<int:qid>/submit/', views.submit, name="submit"),
    path('<int:sid>/scoreboard/', views.scoreboard, name="scoreboard"),
]