from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from mood.question_settings import questions

# Create your views here.

day_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
triggers = []
for i in questions['trigger']:
    triggers.append(questions['trigger'][i])

def index(request):
    if not request.user or not request.user.is_authenticated:
        print("not auth")
        return redirect("login.html")

    today = datetime.date.today()
    dayweek = datetime.date.weekday(today)


    return render(request,"index.html", {
            "today": day_of_week[dayweek]+" "+str(today),
            "questions": questions,
            "triggers" : triggers,

        })

# def login(request):
#     return render(request,"login.html")


def update(request):
    return redirect("timeline")


def timeline(request):
    return render(request, "timeline.html")
