from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"home.html")

def login(request):
    return render(request,"login.html")

def login_warden(request):
    return render(request,"login_warden.html")
