from django.shortcuts import render, redirect
from .forms import CreateNewUser, LinkForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Link




# Create your views here.
def start_page(request):
    return render(request, "linkmodifier/startpage.html")

def register(request):
    form = CreateNewUser()
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, "linkmodifier/registration.html", context)

def login_page(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.info(request, "Username or password is incorrect")
    return render(request, "linkmodifier/login.html")

@login_required()
def home_page(request):
    links = Link.objects.all().filter(user=request.user)

    context = {'links':links}
    return render(request, 'linkmodifier/homepage.html', context)

@login_required()
def add_link(request):
    form = LinkForm()

    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
        return redirect('home_page')

    context = {'form': form}
    return render(request, 'linkmodifier/addlink.html', context)

def logout_view(request):
    logout(request)
    return redirect('start_page')