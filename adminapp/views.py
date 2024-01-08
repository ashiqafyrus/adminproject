from django.shortcuts import render,redirect
from adminapp.models import course
from adminapp.models import student
from adminapp.models import usermember
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import os
def index(request):
    return render(request,'index.html')
def loginpage(request):
    return render(request,'login.html')
def userhome(request):
    return render(request,'userhome.html')
def add_course(request):
    return render(request,'add_course.html')
def admin_home(request):
    return render(request,'admin_home.html')

def log(request):
    print("hello")
    if request.method == "POST":
        uname=request.POST['name']
        print(uname)
        password1=request.POST['password']
        print(password1)
        use=auth.authenticate(username=uname,password=password1)
        if use is not None:
            if use.is_staff:
            
                login(request,use)
                messages.info(request,f'Welcome {uname}')
                return redirect('admin_home')
            else:
                login(request,use)
                auth.login(request,use)
                return redirect('userhome')
        else:
            messages.info(request,'invalid username or password ')
            return redirect('/')
    else:
        return redirect('index')

def addcourse(request):
    if request.method=='POST':
        c=request.POST.get('coursename')
        f=request.POST.get('fees')
        ck=course(course_name=c,fee=f)
        ck.save()
        return redirect('admin_home')
def add_student(request):
    courses=course.objects.all()
    return render(request,'student.html',{'coursekey':courses})
def add_studentdetails(request):
    if request.method=='POST':
        studentname=request.POST['name']
        studentaddress=request.POST['address']
        studentage=request.POST['age']
        studentdate=request.POST['joiningdate']
        studentcourse=request.POST['sel']
        course1=course.objects.get(id=studentcourse)
        s=student(student_name=studentname,student_address=studentaddress,
                  student_age=studentage,joining_date=studentdate,c=course1)
        s.save()
        return redirect('admin_home')
def show_student(request):
    s=student.objects.all()
    return render(request,'show_student.html',{'skey':s})
def edit_student(request,pk):
    s=student.objects.get(id=pk)
    ck=course.objects.all()
    return render(request,'edit_student.html',{'stud':s,'ckey':ck})
def edit_studentdetails(request,pk):
    if request.method=='POST':
        s=student.objects.get(id=pk)
        s.student_name=request.POST['name']
        s.student_address=request.POST['address']
        s.student_age=request.POST['age']
        s.joining_date=request.POST['joiningdate']
        se=request.POST['sel']
        course1=course.objects.get(id=se)
        s.c=course1
        s.save()
        return redirect('show_student')
    return render(request,'edit_student.html')
def delete_student(request,pk):
    p=student.objects.get(id=pk)
    p.delete()
   
    return redirect('show_student')
def add_teacher(request):
    courses=course.objects.all()
    return render(request,'teacher_signin.html',{'courseke':courses})
def add_teacherdetails(request):
    if request.method=='POST':
        teacherfirstname=request.POST.get('tfirstname')
        teacherlastname=request.POST.get('tlastname')
        uname=request.POST.get('username')
        teacherpassword1=request.POST.get('tpassword1')
        teacherpassword2=request.POST.get('tpassword2')
        teacheraddress=request.POST.get('taddress')
        teacherage=request.POST.get('tage')
        teacheremail=request.POST.get('temail')
        teacherphone=request.POST.get('txtEmpPhone')
        teacherfile=request.FILES.get('tfile')
        studentcourse=request.POST['sel']
        course1=course.objects.get(id=studentcourse)
        if teacherpassword1==teacherpassword2:
            if User.objects.filter(username=uname).exists():
                messages.info(request,'user already exist')
                return redirect('add_teacher')
            else:
                use=User.objects.create_user(first_name=teacherfirstname,last_name=teacherlastname,
                                              username=uname,password=teacherpassword1,email=teacheremail)
                use.save()
                s=usermember(address=teacheraddress,age=teacherage,number=teacherphone,image=teacherfile,
                     c=course1,user=use)
                messages.info(request,'success')
        
                s.save()
                return redirect('loginpage')
        else:
            messages.info(request,'password doesnt match')
            return redirect('add_teacher')
    else:
        return redirect('log')
def show_teacher(request):
    s=usermember.objects.all()
    return render(request,'show_teacher.html',{'tkey':s})
def delete_teacher(request,pk):
    p=usermember.objects.get(id=pk)
    p.delete()
   
    return redirect('show_teacher')
def show_usermember(request):
    if request.user.is_authenticated:

        s=usermember.objects.all()
        return render(request,'show_usermember.html',{'tkey':s})
    return redirect('/')

def edit_usermember(request):
    if request.user.is_authenticated:
        current_user=request.user.id
        user=usermember.objects.get(user_id=current_user)
        courses = course.objects.all()
        return render(request, 'edit_usermember.html', {'detail': user, 'ck': courses})

def edit_teacher(request):
    if request.user.is_authenticated:
        courses=course.objects.all()
        current_user=request.user.id
        s=usermember.objects.get(user_id=current_user)
    if request.method=='POST':
        
        s.firs_tname=request.POST.get('fname')
        s.last_name=request.POST.get('lname')
        s.address=request.POST.get('address')
        s.age=request.POST.get('age')
        s.email=request.POST.get('mail')
        s.number=request.POST.get('contact')
        if len(request.FILES)!=0:
            if len(s.image)>0:
                os.remove(s.image.path)
            s.image=request.FILES.get('image_file')
        se=request.POST['sel']
        course1=course.objects.get(id=se)
        s.c=course1
        s.save()
        return redirect('profile')
    return render(request,'edit_usermember.html',{'detail':s,'ck':courses})
def logoutfunction(request):
    auth.logout(request)
    return redirect('index')
def profile(request):
    if request.user.is_authenticated:
        current_user=request.user.id
        s=usermember.objects.get(user_id=current_user)
        return render(request,'profile.html',{'detail':s})
   
def profile_function(request,pk):
    if request.method=='POST':
        s=usermember.objects.get(id=pk)
        s.firstname=request.POST['fname']
        s.lastname=request.POST['lname']
        s.address=request.POST['address']
        s.age=request.POST['age']
        s.email=request.POST['mail']
        s.number=request.POST['contact']
        if len(request.FILES)!=0:
            if len(s.image) > 0:
                os.remove(s.image.path)
            s.image=request.FILES.POST.get('image_file')
        se=request.POST['sel']
        course1=course.objects.get(id=se)
        s.c=course1
        s.save()
        return redirect('userhome')
    return render(request,'profile.html')