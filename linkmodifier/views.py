from django.shortcuts import render
from .forms import CreateNewUser
from django.contrib.auth import login, authenticate

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

def login(request):
    return render(request, "linkmodifier/login.html")