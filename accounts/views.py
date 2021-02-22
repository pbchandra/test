from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib  import messages
from main_app.models import encrypted_data
# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        email= request.POST['email']
        username= request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        print(password1)
        print(password2)
        if password1 != password2:
            messages.info(request," Password and the Confirm Password doesn't match!!")
            return  redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request,"Username has been already taken, please try some other username")
            return  redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"Email has been already registered, please use some other email")
            return  redirect('register')
        else:
            user = User.objects.create_user(username=username,password=password1,email =email,first_name=first_name,last_name=last_name)
            user.save()
            print('user created')
            return redirect('login')
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def login_test(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid credentials")
            return render(request,"login.html")
            

def profile(request):
    
    return render(request,'profile.html')

def profile_update(request):
    username=request.user.username
    first_name= request.POST['first_name']
    email = request.POST['email']
    #password = request.POST['password']
    last_name = request.POST['last_name']
    user=User.objects.filter(username=username).update(email =email,first_name=first_name,last_name=last_name)
    success="saved Successfully"
    suc="alert alert-success"
    return redirect('profile')
    #render(request,'profile.html',{'success':success,'suc':suc})

def rest_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            username=request.user.username
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            success="Password has been changed successfully"
            suc="alert alert-success"
            return render(request,'rest_password.html',{'success':success,'suc':suc})
        else:
            err="password doesn't match"
            er="alert alert-danger"
            return render(request,'rest_password.html',{'success':err,'suc':er})
            
    return render(request,'rest_password.html')

def dashboard(request):
    user_username=request.user.username
    sent_count=encrypted_data.objects.filter(sendby=user_username).count()
    received_count=encrypted_data.objects.filter(sendto=user_username).count()
    return render(request,'dashboard.html',{'sent_count':sent_count,'received_count':received_count})

def logout(request):
    auth.logout(request)
    return redirect('/')
