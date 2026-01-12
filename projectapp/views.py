from django.shortcuts import render,redirect
from .models import Movie
from .forms import ProjectForm

# Create your views here.

def home(request):
    List = Movie.objects.all()
    context = {"data":List}
    return render(request,'index.html',context)

def main(request):
    List = Movie.objects.all()
    context = {"data":List}
    return render(request,'main.html',context)

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
    context = { "FormData":a }
    return render(request,'projects/CreateProjectFrom.html',context)

def UpdateProject(request,i):
    data =  Movie.objects.get(id=i)
    
    form = ProjectForm(instance=data)
    
    if request.method=='POST':
        x = ProjectForm(request.POST,request.FILES,instance=data)
        if x.is_valid():
            x.save()
            return redirect('home')
    context = {"FormData":form}
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
    return render(request,'projects/DeleteForm.html',context)