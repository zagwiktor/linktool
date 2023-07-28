from django.shortcuts import render, redirect
from .forms import CreateNewUser, LinkForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Link
import qrcode
from django.core.files import File
from io import BytesIO






# Create your views here.
def start_page(request):
    return render(request, "linkmodifier/startpage.html")

def register(request):
    form = CreateNewUser()
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f"User: {user}, was created")
            return redirect('login_page')

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

def add_qr(request, pk):
    links = Link.objects.filter(id=pk).values()
    url = str(links[0]['url_link'])

    if request.method == 'POST':
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(url)
        qr_img = qr.make_image()

        qr_byte_array = BytesIO()
        qr_img.save(qr_byte_array)
        qr_file = File(qr_byte_array)

        link_obj = Link.objects.get(id=pk)
        link_obj.png_with_qr.save(f"QrCode{pk}.png", qr_file)
        link_obj.save()
        return redirect('home_page')

    context = {'links':links}
    return render(request, "linkmodifier/add_qr.html", context)