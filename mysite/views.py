from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from .models import *

@login_required(login_url='login-page')
def home(request):
    if request.method=='POST':
        taskValue=request.POST['task']
        # if len(taskValue) < 0:
        #     taskerror = "Iltimos bo'sh topshiriq qo'shmang"
        #     return render(request, 'home.html', {'taskerror': taskerror})
        data=Task(task=taskValue,user=request.user)
        data.save()
        return redirect('home-page')
    task=Task.objects.filter(user=request.user)
    return render(request,'home.html',{'tasks':task})
    return redirect('profile-page')

@login_required(login_url='login-page')
def profilepage(request):
    return render(request, 'profile.html')

def check_user(request):
    username=request.GET.get('username')#admin
    check=User.objects.filter(username=username)#1
    if len(check)>0:
        return HttpResponse('Exists')
    else:
        return HttpResponse('No Exists')
def signup(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['pwd']
        password2 = request.POST['pwd2']
        if len(uname)<5:
            u5="Foydalanuvchi nomi 6 ta belgidan kam bo'lmasligi kerak"
            return render(request,'signup.html',{'u5':u5})
        if len(password1)<8:
            pdw8 = "Kiritilgan parol 8ta belgidan kam bo'lmasligi kerak"
            return render(request, 'signup.html', {'pdw8': pdw8})
        if User.objects.filter(username=uname).exists():
            status = 'Bu username allaqachon mavjud'
            return render(request, 'signup.html', {'status': status})
        if password1 != password2:
            status = 'Birinchi parol tastiqlovchi parolga mos emas'
            return render(request, 'signup.html', {'status': status})
        else:
            usr = User.objects.create_user(username=uname, first_name=firstname, last_name=lastname, email=email,password=password1)
            usr.save()
        return redirect('login-page')
    return render(request, 'signup.html')


def loginForm(request):
    if request.method=='POST':
        username=request.POST.get('uname')
        password=request.POST.get('pwd')
        usr=authenticate(request,username=username,password=password)
        if usr is not None:
            login(request,usr)
            return redirect('profile-page')
        else:
            status="Foydalanuvchi nomi yoki parol noto'g'ri terilgan"
            return render(request,'login.html',{'status':status})
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login-page')
    return render(request,'logout.html')

@login_required(login_url='login-page')
def change_password(request):
    context={}
    if request.method=='POST':
        cpassword=request.POST['cpwd']
        npassword=request.POST['npwd']
        passwordc=request.POST['npwdc']
        usr=User.objects.get(id=request.user.id)
        if npassword!=passwordc:
            msg = 'Birinchi parol tastiqlovchi parolga mos emas'
            context={'msg':msg}
            return render(request,'change_password.html',context)
        if usr.check_password(cpassword):
            usr.set_password(npassword)
            usr.save()
            login(request,usr)
            status='Parol muvaffaqiyatli almashtirildi!'
            col='alert-success'
            context={'status':status,'col':col,}
            return render(request,'change_password.html',context)
        else:
            status = "Avvalgi parol noto'g'ri, parol almashmadi !"
            col = 'alert-danger'
            context = {'status': status, 'col': col}
    return render(request,'change_password.html',context)

def forget_password(request):
    if request.method == 'POST':
        username = request.POST['uname']
        new_password = request.POST['npwd']
        user = get_object_or_404(User, username=username)
        user.set_password(new_password)
        user.save()
        login(request, user)
        return redirect('home-page')
    return render(request,'forget_password.html')


import random
from django.core.mail import EmailMessage
def reset_password(request):
    username=request.GET['username']
    try:
        usr=get_object_or_404(User,username=username)
        otp=random.randint(100000,999999)
        msg=f"Hurmatli {usr.last_name} {usr.first_name} \nSizga parolingizni yangilash maqsadida {otp} - ushbu bir martalik kod yuborildi. Iltimos ushbu kodni uchinchi shaxsga bermang ! " \
            f"\nHurmat bilan Xabibullaxanov A"
        try:
            em=EmailMessage('Parolni tiklash',msg,to=[usr.email])
            em.send()
            return JsonResponse({'status':'sent','email':usr.email,'otp':otp})
        except:
            return JsonResponse({'status':'failed','email':usr.email})
    except:
        return JsonResponse({'status':'error'})

def error_404(request,exception):
    return render(request,'error_404.html')

def task_delete(request,pk):
    Task.objects.filter(id=pk).delete()
    return redirect('home-page')

def task_edit(request,pk):
    data=Task.objects.get(id=pk)
    if request.method == 'POST':
        taskValue = request.POST['task']
        Task.objects.filter(id=pk).update(task=taskValue)
        return redirect('home-page')
    return render(request,'task_edit.html',{'task':data})

@login_required(login_url='login-page')
def contact(request):
    print(request.POST)
    context={}
    if request.method=='POST':
        ism=request.POST['ism']
        email=request.POST['email']
        mavzu=request.POST['mavzu']
        xabar=request.POST['xabar']
        data=Contact(fio=ism,email=email,topic=mavzu,message=xabar)
        data.save()
        status=f'Sizning xabaringiz muvaffaqiyatli yuborildi!'
        context = {'status': status}
    return render(request,'contact.html',context)


