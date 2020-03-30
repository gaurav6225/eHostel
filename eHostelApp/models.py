from django.db import models

# Create your models here.
class Allstudents(models.Model):
    join_year   =  models.InterField(default = 2017)
    roll_no     =  models.CharField(max_length = 10, primary_key = True,unique = True)

class Hostel(models.Model):
    pass

class St_details(models.Model):
    pass

class Admin(models.Model):
    pass

class Room(models.Model):
    pass

class Swap(models.Model):
    pass

class teammate(models.Models):
    pass
