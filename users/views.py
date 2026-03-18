from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.db.models import F
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from projectapp.models import Movie
from .forms import ProfileForm
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.



def profiles(request):
    qs = Profile.objects.all()

    if request.user.is_authenticated and not request.user.is_superuser:
        qs = qs.exclude(user=request.user)

    context = {
        "Profiles": qs
    }
    return render(request, 'users/profiles.html', context)

def user_profile(request, i):
    Profile.objects.filter(id=i).update(views=F('views') + 1)
        
    profile = get_object_or_404(Profile, id=i)
    
    return render(request, 'users/user_profile.html', {
        'user_profile': profile,
        'views': profile.views,
    })

# def LoginUser(request):
#     page = 'Login'
#     if request.user.is_authenticated:
#         return redirect('profiles')
    
#     if request.method == 'P~~OST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         try:
#             user=User.objects.get(username=username)
#         except:
#             messages.error(request,'Username does not exist')
#             return render(request,'login.html')
#         user=authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             messages.success(request,'User was login')
#             return redirect('profiles')
#         else:
#             messages.error(request,'Username OR password is incorrect')
    
#     context={"page":page}
#     return render(request,'login.html',context)

def LoginUser(request):
    page = 'Login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password = request.POST.get('password')

        # Convert email → username if needed
        if '@' in username_input:
            try:
                user_obj = User.objects.get(email__iexact=username_input)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, 'Invalid username/email or password')
                return render(request, 'users/login.html', {"page": page})
        else:
            username = username_input

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User logged in successfully')
            return redirect('profiles')
        else:
            messages.error(request, 'Invalid username/email or password')

    return render(request, 'users/login.html', {"page": page})


def LogoutUser(request):
    logout(request)
    messages.success(request,'User was logged out!')
    return redirect('LoginUser')


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
    return render(request, 'users/login.html', context)

@login_required
def CreateProfile(request):
    if request.user.is_superuser:
        return redirect('index')  
    
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'users/profile.html', {'form': form})

# @login_required
# def EditProfile(request):
#     if request.user.is_superuser:
#         return redirect('index')

#     profile = request.user.profile
#     form = ProfileForm(instance=profile)

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('EditProfile')

#     return render(request, 'editprofile.html', {'form': form})

@login_required
def my_profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'users/user_profile.html', {
        'user_profile': user_profile,
        'views': user_profile.views,
    })

from django.shortcuts import redirect
from .forms import ProfileForm

@login_required
def EditProfile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        new_username = request.POST.get("username")

        # check if username exists
        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            form.add_error("username", "Username already taken")

        if form.is_valid():

            request.user.username = new_username
            request.user.save()

            form.save()

            return redirect("my-profile")

    else:
        form = ProfileForm(instance=profile)

    return render(request, "users/editprofile.html", {
        "form": form
    })