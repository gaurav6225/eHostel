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

@login_required
def register_post(request):
    if request.method == 'POST':
        student_name = request.POST['student_name']
        reg_no = request.POST['reg_no']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        gender = request.POST['gender']
        #date_of_birth = request.POST['date_of_birth']
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
            cursor.execute("INSERT INTO eHostelApp_student (student_name,reg_no,email,phone_no,gender,guardian_name,guardian_phone,address,city,state,pincode,branch,year,mess_fee,academic_fee) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d,%s,%d,%s,%s)"
                                                          %(student_name,reg_no,email,phone_no,gender,guardian_name,guardian_phone,address,city,state,pincode,branch,year,mess_fee,academic_fee))
        return HttpResponseRedirect(reverse('dashboard'))



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
            cursor.execute("SELECT * FROM eHostelApp_room WHERE student_1_id = %s OR student_2_id = %s"%(request.user.username,request.user.username))
            records = cursor.fetchall()
            valid = (len(records)==0)
            if not valid:
                messages.add_message(request,messages.ERROR,"YOUR ROOM IS ALREADY ALLOCATED")
                return HttpResponseRedirect(reverse('allocate')) 
            cursor.execute("SELECT * FROM eHostelApp_room WHERE h_name = %s AND room_no = %d"%(h_name,int(room_no)))
            records = cursor.fetchall()
            valid_room = (len(records) == 0)
            if not valid_room:
                messages.add_message(request,messages.ERROR,"ROOM IS ALREADY FULL PLEASE TRY ANOTHER")
                return HttpResponseRedirect(reverse('allocate'))
            cursor.execute("SELECT * FROM eHostelApp_roommate WHERE (student_1_id=%s OR student_2_id=%s) AND accept = 1"%(request.user.username,request.user.username))
            records = cursor.fetchone()
            valid = (len(records) == 1)
            if not valid:
                messages.add_message(request,messages.ERROR,"PLEASE CHOOSE YOUR ROOMMATE FIRST")
                return HttpResponseRedirect(reverse('allocate'))
            student_1,student_2 = records[2],records[3]
            cursor.execute("INSERT INTO eHostelApp_room (room_no,h_name,student_1_id,student_2_id) VALUES (%s,%s,%s,%s)"%(room_no,h_name,student_1,student_2))
            return HttpResponseRedirect(reverse('success'))
    else:
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
def vacancy(request):
    if request.method == 'POST':
        h_name = request.POST['h_name']
        room_no = request.POST['room_no']
        with connection.cursor() as cursor:
            cursor.execute("SELECT capacity FROM eHostelApp_hostel WHERE h_name = %s"%(h_name))
            records = cursor.fetchone()
            capacity = records[0]
            if room_no > capacity or room_no < 0:
                messages.add_message(request,messages.ERROR,"INVALID ROOM NUMBER")
                return HttpResponseRedirect(reverse('vacancy'))
            cursor.execute("SELECT * FROM eHostelApp_room WHERE h_name = %s AND room_no = %d"%(h_name,int(room_no)))
            records = cursor.fetchall()
            vacant_room = (len(records) == 0)
            if vacant_room:
                res = {
                    'display' : "SELECTED ROOM IS VACANT",
                }
            else:
                res = {
                    'display' : "SELECTED ROOM IS OCCUPIED",
                }
            return render(request,'/eHostelApp/show_vacancy.html',res)
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT h_name FROM eHostelApp_hostel")
            records = cursor.fetchall();
            all_hostel = [i[0] for i in records]
            res = {
                'all_hostel' : all_hostel,
            } 
            return render(request,'/check_vacancy.html',res)

@login_required
def show_student(request):
    if request.method == 'POST':
        reg_no = request.POST['reg_no'] 
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM eHostelApp_students WHERE reg_no=%s"%(reg_no))
            records = cursor.fetchone()
            valid = (len(records) == 1)
            res = {
                'valid'   : valid,
                'details' : records,
            }
            return render(request,'/eHostelApp/details.html',res)

    else:
        valid = is_war(request.user.id)
        render(request,'/eHostelApp/show_student.html',{'valid':valid})

@login_required
def roommate_req(request):
    if request.method == 'POST':
        roll_no = str(request.POST['roll_no'])
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM auth_user WHERE username = %s"%(roll_no))
            records = cursor.fetchall()
            not_valid = (len(records) == 0) or (roll_no==request.user.username)
            if not_valid :
                res = {
                    'mes' : 1,
                    'print' : "PLEASE CHOOSE A VALID ROLL NUMBER"
                }
            else:
                cursor.execute("INSERT INTO eHostelApp_roommate (student_1_id,student_2_id) VLAUES (%s,%s)"%(request.user.username,roll_no))
                res = {
                    'mes' : 1,
                    'print' : "REQUEST SENT SUCCESSFULLY"
                }
            render(request,'/eHostelApp/roommate_req.html',res)

    else:
        render(request,'/eHostelApp/roommate_req.html',{'mes':0})

@login_required
def roommate_acpt(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id,student_1_id FROM eHostelApp_roommate WHERE accept=0 AND student_2_id=%s"%(request.user.username))
        res = cursor.fetchall()
        temp = [dict(zip(["id","student"],i)) for i in res]
        return render(request,'/eHostelApp/roommate_acpt.html',temp)

@login_required
def action(request,operation,id):
    if operation == 'accept':
        with connection.cursor() as cursor:
            cursor.execute("SELECT student_1_id,student_2_id FROM HostelApp_roommate  WHERE id = %d" %(id))
            students = cursor.fetchone()
            stu1 = students[0]
            stu2 = students[1]
            cursor.execute("SELECT * FROM eHostelApp_roommate  WHERE accept=1 AND ((student_1_id=%s OR student_2_id=%s) OR (student_1_id=%s OR student_2_id=%s)) "%(stu1,stu1,stu2,stu2))
            records = cursor.fetchall()
            if len(records) == 0:
               cursor.execute("UPDATE eHostelApp_roommate SET accept = 1 WHERE id = %d"%(id))
               messages.add_message(request,messages.SUCCESS,"ROOMMATE ADDED SUCCESSFULLY")
            else:
                messages.add_message(request,messages.ERROR,"ERROR AS ROOMMATE ALREADY EXISTS")
            return HttpResponseRedirect(reverse('roommate_acpt'))
    else:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM eHostelApp_roommate WHERE id=%d"%(int(id)))
            return HttpResponseRedirect(reverse('roommate_acpt'))



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