from django.contrib import admin

# Register your models here.
from .models import Feeling
admin.site.register([Feeling])
