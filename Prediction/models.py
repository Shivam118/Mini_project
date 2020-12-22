from django.db import models

# Create your models here.

class Donater(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_id = models.CharField(max_length=50)
    address = models.CharField(max_length=120)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip = models.IntegerField(default=000000)
    payment = models.CharField(max_length=10,default="UPI")
    plan = models.CharField(max_length=10,default="Silver")
    
def __str__(self):
    return self.first_name +" " + self.last_name