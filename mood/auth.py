from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Auth-related routes
def signup(request):
    print(333)
    if request.method == "GET":
        return render(request, "./signup.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        firstname = request.POST["firstname"]
        email = request.POST["email"]
        try:
            user = User.objects.create_user(username=username, password=password, first_name=firstname,email=email)
            if user is not None:
                return login(request)
        except:
            return render(request, "./signup.html", {"error": "Signup failed. User exists?"})

        return HttpResponse("Posted to signup")

def login(request):
    print(444)
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            return render(request, "./login.html",{"error": "Invalid credentials."})

def logout(request):
    auth.logout(request)
    return redirect('index')
