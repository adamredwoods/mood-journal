"""moodjournal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from mood import views
import mood.auth
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', mood.auth.login, name="login"),
    path('login/<int:guest>/', mood.auth.login, name="login_guest"),
    path('logout/', mood.auth.logout, name="logout"),

    path('signup/', mood.auth.signup, name="signup"),
    path('timeline/', views.timeline, name="timeline"),
    path('timeline/data/', views.timeline_data, name="timeline_data"),
    path('timeline/data/<int:date>/', views.timeline_data_date, name="timeline_data_date"),
    path('create/', views.create, name="create"),
    path('edit/', views.edit_all, name="edit"),
    path('edit/delete/', views.delete_feeling, name="delete"),
    path('edit/<slug:monthyear>/', views.edit_all, name="editmonth"),

]
