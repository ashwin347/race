from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from .models import studentDetails
# Create your views here.
def adminLoginPage(request): #returns admin login page template
    return render(request,template_name='adminLogin.html')
@csrf_exempt
def adminLoginValidation(request):          # validates user login
    username=request.POST['username']
    password=request.POST['password']
    if username=='admin' and password=='admin':  # returns admin home template  if username and password is admin
        return render(request,'adminLeftPane.html')
    else:
        return render(request,'adminLogin.html',{'error':'True'})

def viewStudentDetails(request):  # returns all the details of students
    students=studentDetails.objects.all()
    return render(request,'studentDetails.html',{'studentDetails':students})
def addStudentDetails(request):
    name=request.POST['name']
    phone=request.POST['phone']
    email=request.POST['email']
    newStudentData=studentDetails(name,email,phone)
    newStudentData.save()
    return render(request,'adminHome.html',{'status':'Student Data Successfully added'})
def a(request):
    return render(request,'adminLeftPane.html')