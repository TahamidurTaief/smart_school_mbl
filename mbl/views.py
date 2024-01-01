from django.shortcuts import redirect, render, HttpResponse
from app.EmailBackEnd import EmailBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import *



def base(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'website/home.html')

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
    # student_obj = Student.objects.get(admin=userId)


    if userId.user_type == "3":
        return redirect('student_my_profile')

    elif userId.user_type == "2":
        return redirect('teacher_my_profile')

    elif userId.user_type == "1":
        return redirect('admin_home')


    context = {
        'userId': userId,
    }
    return render(request, 'profile.html', context)





def profileUpdate(request):
    if request.method == "POST":
        try:
            password = request.POST.get('password')

            userId = CustomUser.objects.get(id=request.user.id)
            userId.set_password(password)
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