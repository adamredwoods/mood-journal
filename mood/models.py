from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feeling(models.Model):
    feeling = models.CharField(max_length=200)
    trigger = models.CharField(max_length=100, default="")
    trigger2 = models.CharField(max_length=100, default="")
    trigger3 = models.CharField(max_length=100, default="")
    journal = models.TextField()
    #time in seconds
    date = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.feeling+", "+self.trigger+", "+str(self.date) 
