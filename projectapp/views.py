from django.shortcuts import render,redirect
from .models import Movie
from .forms import ProjectForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()
# Create your views here.

def home(request):
    q = request.GET.get('q', '').strip()

    data = Movie.objects.all()

    if q:
        data = data.filter(
            Q(title__icontains=q) |
            Q(desc__icontains=q)
        ).distinct()

    context = {
        "data": data,
        "search": q,
    }

    return render(request,'index.html',context)


def projects(request,i):
    List = Movie.objects.get(id=i)
    context={"Singleproject":List}
    return render(request,'projects/project.html',context)

def CreateProject(request):
    
    a = ProjectForm()
    
    if request.method=='POST':
        x = ProjectForm(request.POST,request.FILES)
        if x.is_valid():
            x.save()
            return redirect('home')
    context = { "FormData":a,
               "is_edit": False,}
    return render(request,'projects/CreateProjectFrom.html',context)

def UpdateProject(request,i):
    data =  Movie.objects.get(id=i)
    
    form = ProjectForm(instance=data)
    
    if request.method=='POST':
        x = ProjectForm(request.POST,request.FILES,instance=data)
        if x.is_valid():
            x.save()
            return redirect('home')
    context = {"FormData":form,
               "is_edit": True,}
    return render(request,'projects/CreateProjectFrom.html',context)
    
    
def DeleteProject(request,i):
    
    data =  Movie.objects.get(id=i)
    
    if request.method=='POST':
        action = request.POST.get("action")
        if action == 'Confirm':
            data.delete()
            return redirect('home')
        else:
            return redirect("home")  
    context = {"FormData": data}
    return render(request,'projects/index.html',context)


@login_required
def Projectlist(request):
    q = request.GET.get('q', '').strip()

    # get current user's profile
    profile = request.user.profile

    # filter projects by profile
    data = Movie.objects.filter(owner=profile)

    if q:
        data = data.filter(
            Q(title__icontains=q) |
            Q(desc__icontains=q)
        ).distinct()

    context = {
        "data": data,
        "search": q,
    }

    return render(request, 'projects/ProjectList.html', context)