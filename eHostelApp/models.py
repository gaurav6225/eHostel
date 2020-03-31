from django.db import models

# Create your models here.
class StudentID(models.Model):
    year         =  models.IntegerField(default = 2)
    roll_no      =  models.CharField(max_length = 10, primary_key = True, unique = True)
    password     =  models.CharField(max_length = 40)
    def __str__(self):
		return self.roll_no

class Hostel(models.Model):
    h_name       =  models.CharField(max_length = 20, primary_key = True, unique = True)
    year_alloted =  models.IntegerField(default = 1)
    capacity     =  models.IntegerField(default = 100)
    def __str__(self):
		return self.h_name

class StudentDetails(models.Model):
    student_name = models.CharField(max_length = 100)
    reg_no = models.CharField(max_length = 10,primary_key = True,unique = True)
    email = models.EmailField(max_length = 25)
    phone_no = models.CharField(max_length = 10)
    GENDER_CHOICES = [
        ('male','Male'),
        ('female','Female')
    ]
    gender = models.CharField(choices = GENDER_CHOICES,default = 'male',max_length = 6)
    date_of_birth = models.DateField()
    guardian_name = models.CharField(max_length = 100)
    guardian_phone = models.CharField(max_length = 10)
    address       =   models.CharField(max_length=100)
    city          =  models.CharField(max_length = 100,null =True)
    state         =  models.CharField(max_length = 100,null =True)
    pincode       =  models.IntegerField()
    branch        =  models.CharField(max_length = 50)
    year          = models.IntegerField(default = 2)
    def __str__(self):
		return self.student_name

class Admin(models.Model):
    username    =  models.CharField(max_length = 20, primary_key = True, unique = True)
    password    =  models.CharField(max_length = 40)
    def __str__(self):
		return self.username

class Room(models.Model):
    room_no     =  models.IntegerField()
    student_1   =  models.ForeignKey(StudentDetails , on_delete = models.CASCADE)
    student_2   =  models.ForeignKey(StudentDetails , on_delete = models.CASCADE)
    h_name      =  models.ForeignKey(Hostel,on_delete = models.CASCADE)
    def __str__(self):
		return str(self.room_no)

class Swap(models.Model):
    student_1   =  models.ForeignKey(StudentDetails , on_delete = models.CASCADE)
    student_2   =  models.ForeignKey(StudentDetails , on_delete = models.CASCADE)
    accept      =  models.BooleanField(default = False)

class roommate(models.Models):
    student_1   =  models.ForeignKey(StudentDetails , on_delete = models.CASCADE)
    student_2   =  models.ForeignKey(StudentDetails , on_delete = models.CASCADE)
    accept      =  models.BooleanField(default = False)
