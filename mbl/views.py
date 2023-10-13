from django.shortcuts import redirect, render, HttpResponse
from app.EmailBackEnd import EmailBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import *



def base(request):
    return render(request, 'base.html')

def custom_login(request):
    return render(request, 'login.html')

def doLogin(request):

    if request.method == "POST":
        user = EmailBackend.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password'),)
        
        if user != None:
            login(request, user)  # Use the renamed login function
            user_type = user.user_type
            if user_type == "1":
                return redirect('admin_home')
            
            elif user_type == "2":
                return redirect('staff_home')
            
            elif user_type == "3":
                return redirect('student_home')
            
            elif user_type == "4":
                return redirect('staff2_home')
            
            else:
                messages.error(request, "Incorrect email or password!")
        
        else:
            messages.error(request, "Invalid email or password!")
        
        return redirect('login')  # Redirect to your custom login view


def doLogout(request):
    logout(request)
    return redirect('login')

def profile(request):
    userId = CustomUser.objects.get(id=request.user.id)
    
    context = {
        'userId': userId,
    }
    return render(request, 'profile.html', context)

def profileUpdate(request):
    if request.method == "POST":
        try:
            userId = CustomUser.objects.get(id=request.user.id)
            profile_pic = request.FILES.get('profile_pic')
            userId.first_name = request.POST.get('first_name')
            userId.last_name = request.POST.get('last_name')
            userId.email = request.POST.get('email')
            userId.username = request.POST.get('username')
            password = request.POST.get('password')
            # print(userId.profile_pic)

            if password != None and password != "":
                userId.set_password(password)

            if profile_pic != None and profile_pic != "":
                userId.profile_pic = profile_pic
                
            userId.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect('profile')
        except:
            messages.error(request, "Failed to Update Profile!")
            return redirect('profile')
    else:
        return redirect('profile')


def Notice(request):
    notice_obj = Notice.objects.all()

    context = {
        'notice_obj' : notice_obj,
    }
    return render(request, 'includes/header.html')