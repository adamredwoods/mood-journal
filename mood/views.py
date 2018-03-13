from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import time
from mood.question_settings import questions
from .models import Feeling
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


# Create your views here.

day_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
month_array = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
triggers_ordered = []

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

##align the array of trigger responses to the array of feelings
##doing this because django templating really doesn't do well with arrays in dicts
for i,f in enumerate(questions['feeling']):
    triggers_ordered.append(questions['trigger'].get(f))


def index(request):
    if not request.user or not request.user.is_authenticated:
        print("not auth")
        return redirect("login")

    today = datetime.date.today()
    dayweek = datetime.date.weekday(today)
    ##day_of_week[dayweek]+" "+

    return render(request,"index.html", {
            "today": str(today),
            "questions": questions,
            "triggers_ordered" : triggers_ordered,
        })


def create(request):
    if request.user and request.user.is_authenticated:
        time_s =0
        if "time" in request.POST:
            time_input =request.POST["time"]
            time_s = datetime.datetime.strptime(time_input, '%Y-%m-%d')
            time_s = time_s.timestamp() * 1000
        else:
            time_s = int(time.time() * 1000) ## time in mseconds

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
        return redirect("login")

    feeling_set = Feeling.objects.filter(user_id=request.user.id)

    #feelings_json = json.dumps(feeling_set, cls=DjangoJSONEncoder)
    feelings_json = serializers.serialize("json", feeling_set)

    return render(request, "timeline.html", { "feeling_axis": questions['feeling'], "feeling_color": questions['feeling_bgcolor']} )

## use this to send the timeline data to the client
## TODO: get data for only the current year
def timeline_data(request):
    if request.user and request.user.is_authenticated:

        feeling_set = Feeling.objects.filter(user_id=request.user.id)
        feelings_json = serializers.serialize("json", feeling_set)
        return HttpResponse(feelings_json, content_type='application/json')

def timeline_data_date(request, date):
    if request.user and request.user.is_authenticated:

        f = Feeling.objects.filter(user_id=request.user.id, date=date)
        json = serializers.serialize("json", f)
        return HttpResponse(json, content_type='application/json')

def delete_feeling(request):
    if not request.user or not request.user.is_authenticated:
        print("not auth")
        return redirect("login")
    if (request.method != "POST"):
        return redirect("/edit/")

    id = request.POST["id"]
    f = Feeling.objects.get(id=int(id))
    if (not f):
        return HttpResponse("Id not found.")
    res = f.delete()
    return HttpResponse("delete")

def edit_all(request, monthyear=""):
    if not request.user or not request.user.is_authenticated:
        print("not auth")
        return redirect("login")

    dt = None
    if (not monthyear):
        dt = datetime.datetime.fromtimestamp(time.time()) ## time in seconds
        monthyear = str(dt.month)+"-"+str(dt.year)

    year = int(monthyear.split("-")[1])
    month = int(monthyear.split("-")[0])

    if (month>1):
        prev_dt = datetime.datetime(year, month-1, 1)
    else:
        prev_dt = datetime.datetime(year-1, 12, 1)
    if (month<12):
        next_dt = datetime.datetime(year, month+1, 1)
    else:
        next_dt = datetime.datetime(year+1, 1, 1)


    ## convert string into millsecs epoch
    startms = time.mktime(datetime.datetime(year, month, 1).timetuple())*1000
    stopms = time.mktime(datetime.datetime(year, month, last_day_of_month(datetime.datetime(year, month, 1)).day ).timetuple())*1000+86399
    #print (startms, stopms)

    feeling_set = Feeling.objects.filter(user_id=request.user.id, date__gte=int(startms), date__lte=int(stopms) )
    feeling_arr = []

    ## sort by day, and remove duplicates (get most recent)
    feeling_set = sorted(feeling_set, key=lambda feel: feel.date, reverse=True)
    for f in feeling_set:
        f.date = datetime.date.fromtimestamp(f.date/1000.0)
        feeling_arr.append(f)

    nav_prev = str(prev_dt.month)+"-"+str(prev_dt.year)
    nav_next = str(next_dt.month)+"-"+str(next_dt.year)
    cur_date = str(month_array[month-1])+" "+str(year)

    return render(request, "edit_all.html", {
        "feeling_data": feeling_arr,
        "questions": questions,
        "triggers_ordered" : triggers_ordered,
        "nav_prev": nav_prev,
        "nav_next": nav_next,
        "cur_date": cur_date,
    } )
