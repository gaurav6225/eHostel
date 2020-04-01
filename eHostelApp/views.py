from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
import datetime
import MySQLdb as mdb
import hashlib

# Create your views here.

def home(request):
    return render(request,"home.html")

def login(request):
    return render(request,"login.html")

def login_warden(request):
    return render(request,"login_warden.html")

def verify_for_registration(request):
    roll_no = request.POST.get('roll_no')
    password = request.POST.get('password')
    if roll_no and password :
        password = conv_to_sha(password)
        cursor = connection.cursor()
        sql_query = "SELECT * FROM StudentID WHERE roll_no =" + " '" + roll_no + "' "
                    +"AND password" + " '" + password + "';"
        cursor.excute(sql_query)
        records = cursor.fetchall()
        valid_id = (len(records) == 1)
        message = "Please try to login again"
        if(not valid_id):
            message = "Not a valid roll number or password"

def interface(request):
    pass


############### Helper Functions ###############

def conv_to_sha(password):
	return(hashlib.sha1(password).hexdigest())
