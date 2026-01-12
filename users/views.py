from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from .models import Profile
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def profiles(request):
    Data = Profile.objects.all()
    context= {"Profiles":Data}
    return render(request,'profiles.html',context)

def user_profile(request,i):
    Data = Profile.objects.get(id=i)
    context = {"user_profile":Data}
    return render(request,'user_profile.html',context)

def LoginUser(request):
    page = 'Login'
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')
            return render(request,'login.html')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'User was login')
            return redirect('profiles')
        else:
            messages.error(request,'Username OR password is incorrect')
    
    context={"page":page}
    return render(request,'login.html',context)


def LogoutUser(request):
    logout(request)
    messages.success(request,'User was logged out!')
    return redirect('LoginUser')

def account():
    pass

# def registerUser(request):
#     page="Register"
#     form=UserCreationForm()

#     if request.method == 'POST':
#         form=UserCreationForm(request.POST)
#         if form.is_valid():
#             user=form.save(commit=False)
#             user.username=user.username.lower()
#             user.save()

#             messages.success (request,'User account was created!')

#             login(request,user)
#             return redirect('profiles')
#         else :
#             messages.error (request,'An error has occurred during registration')            

#     context={'page':page,'form':form}
#     return render(request,'login.html',context)


def registerUser(request):
    page="Register"
    form=CustomUserCreationForm()

    if request.method == 'POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()

            messages.success (request,'User account was created!')

            login(request,user)
            return redirect('profiles')
        else :
            messages.error (request,'An error has occurred during registration')            

    context={'page':page,'form':form}
    return render(request,'login.html',context)
