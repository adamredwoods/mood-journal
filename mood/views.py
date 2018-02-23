from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import time
from mood.question_settings import questions
from .models import Feeling
import json

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


def create(request):
    if request.user and request.user.is_authenticated:
        time_s =0
        if "time" in request.POST:
            time_s =request.POST["time"]
        else:
            time_s = int(time.time() * 1000) ## time in seconds

        new_feeling = Feeling()
        new_feeling.trigger = request.POST["trigger"]
        new_feeling.feeling = request.POST["feeling"]
        new_feeling.journal = request.POST["journal"]
        new_feeling.date = time_s
        new_feeling.user_id = request.user.id
        new_feeling.save()

        return redirect("timeline")


def timeline(request):
    if not request.user or not request.user.is_authenticated:
        print("not auth")
        return redirect("login.html")

    feeling_set = Feeling.objects.filter(user_id=request.user.id)
    feeling_arr = []

    ## sort by day, and remove duplicates (get most recent)
    
    for f in feeling_set:
        print(f)
        feeling_arr.append(f)

    return render(request, "timeline.html", { "feeling_data": feeling_arr } )
