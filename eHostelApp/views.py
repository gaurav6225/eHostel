from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import Http404
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user
from django.core.exceptions import PermissionDenied
import datetime
import MySQLdb as mdb
import hashlib

# Create your views here.

def home(request):
    if request.user:
	    return HttpResponseRedirect(reverse('register'))
    else:
	    return HttpResponseRedirect(reverse('login'))

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('register'))
    else:
        return render(request,'eHostelApp/login.html')

def login_post(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login_user(request,user)
            if is_war(user.id):
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponseRedirect(reverse('register'))
        else:
            messages.add_message(request,messages.ERROR,"Invalid password. Please try again.")
            return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def register(request):
    if is_reg(request.user.id):
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        year = which_year(request.user.id)
        res = {
            'reg_no' : request.user.username,
            'year'   : year,
        }
        return render(request,'eHostelApp/register.html',res)


def register_post(request):
    if request.method == 'POST':
        student_name = request.POST['student_name']
        reg_no = request.POST['reg_no']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        gender = request.POST['gender']
        date_of_birth = request.POST['date_of_birth']
        guardian_name = request.POST['guardian_name']
        guardian_phone = request.POST['guardian_phone']
        address       =   request.POST['address']
        city          =  request.POST['city']
        state         =  request.POST['state']
        pincode       =  request.POST['pincode']
        branch        =  request.POST['branch']
        year          =  request.POST['year']
        mess_fee      =  request.POST['mess_fee']
        academic_fee  =  request.POST['academic_fee']
        #no_due_receipt = request.POST['no_due_receipt']
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO eHostelApp_students (student_name,reg_no,email,phone_no,gender,date_of_birth,guardian_name,guardian_phone,address,city,state,pincode,branch,year,mess_fee,academic_fee) VALUES (%s,%s,%s,%s)")



@login_required
def dashboard(request):
    if is_reg(request.user.id):
        is_warden = is_war(request.user.id)
        context = {
            'is_warden' : is_warden,
        }
        return render(request,'eHostelApp/dashboard.html',context)
    else:
        return HttpResponseRedirect(reverse('register'))

@login_required
def allocate(request):
    if not is_reg(request.user.id):
        return HttpResponseRedirect(reverse('register'))
    year = which_year(request.user.id)
    with connection.cursor() as cursor:
        cursor.execute("SELECT h_name FROM eHostelApp_hostel WHERE year=%d"%(year))
        records = cursor.fetchall()
        hostel_list = [i[0] for i in records]
        res = {
            'hostel_list': hostel_list,
        }
    return render(request,'eHostelApp/allocate.html',res)

@login_required 
def allocate_post(request):
    if request.method == 'POST':
        h_name = request.POST['h_name']
        room_no = request.POST['room_no']
        with connection.cursor() as cursor:
            cursor.execute("SELECT capacity FROM eHostelApp_hostel WHERE h_name = %s"%(h_name))
            records = cursor.fetchone()
            capacity = records[0]
            if room_no > capacity or room_no < 0:
                messages.add_message(request,messages.ERROR,"INVALID ROOM NUMBER")
                return HttpResponseRedirect(reverse('allocate'))
            cursor.excute("SELECT * FROM eHostelApp_room WHERE student_1 = %s OR student_2 = %s"%(request.user.username,request.user.username))
            records = cursor.fetchall()
            valid = (len(records)==0)
            if not valid:
                messages.add_message(request,messages.ERROR,"YOUR ROOM IS ALREADY ALLOCATED")
                return HttpResponseRedirect(reverse('dashboard')) 
            cursor.execute("SELECT * FROM eHostelApp_room WHERE h_name = %s AND room_no = %d"%(h_name,int(room_no)))
            records = cursor.fetchall()
            valid_room = (len(records) == 0)
            if not valid_room:
                messages.add_message(request,messages.ERROR,"ROOM IS ALREADY FULL PLEASE TRY ANOTHER")
                return HttpResponseRedirect(reverse('allocate'))
            cursor.execute("SELECT * FROM eHostelApp_roommate WHERE student_1=%s")
            

@login_required 
def swap(request):
    pass 

############### Helper Functions ###############

def conv_to_sha(password):
	return(hashlib.sha1(password).hexdigest())

def is_reg(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT is_registered FROM eHostelApp_myuser WHERE user_id=%d;"%int(user_id))
        records = cursor.fetchone()
        res = records[0]
    return res

def is_war(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT is_warden FROM eHostelApp_myuser WHERE user_id=%d;"%int(user_id))
        records = cursor.fetchone()
        res = records[0]
    return res
        
def which_year(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT year FROM eHostelApp_myuser WHERE user_id=%d;"%int(user_id))
        records = cursor.fetchone()
        res = records[0]
    return res