from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Auth-related routes
def signup(request):

    if request.method == "GET":
        return render(request, "./signup.html", {"error":""})
    elif request.method == "POST":
        if (request.POST["password"] !="" and
            request.POST["username"] !="" and
            request.POST["email"] !="" and
            request.POST["password"] == request.POST["password2"]):

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
        else:
            msg ="Please fill out the fields."
            if (request.POST["password"] != request.POST["password2"]): msg="Password verify does not match."
            return render(request, "./signup.html", {
                "error": msg,"username": request.POST["username"], "email": request.POST["email"], "firstname": request.POST["firstname"]
            })

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
