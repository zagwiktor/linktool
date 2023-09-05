import random
import string

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.sites.shortcuts import get_current_site
from .forms import CreateNewUser, LinkForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Link
import qrcode
from django.core.files import File
from io import BytesIO
import os

def generate_qr_code(request, pk, url):
    fill_color = request.POST.get('fill-color')
    background_color = request.POST.get('background-color')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr_img = qr.make_image(fill_color=fill_color, back_color=background_color)

    qr_byte_array = BytesIO()
    qr_img.save(qr_byte_array)
    qr_file = File(qr_byte_array)

    link_obj = Link.objects.get(id=pk)
    link_obj.png_with_qr.save(f"QrCode{pk}.png", qr_file)
    link_obj.save()

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

@login_required
def home_page(request):
    links = Link.objects.all().filter(user=request.user)
    context = {'links':links}
    return render(request, 'linkmodifier/homepage.html', context)

@login_required
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

@login_required
def logout_view(request):
    logout(request)
    return redirect('start_page')

@login_required
def add_qr(request, pk):
    links = Link.objects.filter(id=pk).values()
    url = str(links[0]['url_link'])

    if request.method == 'POST':
        generate_qr_code(request, pk, url)
        return redirect('home_page')

    context = {'links':links}
    return render(request, "linkmodifier/add_qr.html", context)

@login_required
def delete_link(request, pk):
    link = get_object_or_404(Link, pk=pk)
    context = {"link":link}

    if request.method=='POST':
        link.delete()
        folder_dir = "linkmodifier/media/images"
        for qr_code in os.listdir(folder_dir):
            if qr_code == f"QrCode{pk}.png":
                os.remove(folder_dir+'/'+qr_code)
        return redirect('home_page')

    return render(request, "linkmodifier/delete.html", context)

@login_required
def edit_qr(request, pk):
    #poprawić edit
    links = Link.objects.filter(id=pk).values()
    url = str(links[0]['url_link'])
    context = {'links': links}
    if request.method == 'POST':
        link = get_object_or_404(Link, pk=pk)
        if link.png_with_qr:
            link.png_with_qr = None
            link.save()
        folder_dir = "linkmodifier/media/images"
        for qr_code in os.listdir(folder_dir):
            if qr_code == f"QrCode{pk}.png":
                os.remove(folder_dir + '/' + qr_code)
        generate_qr_code(request, pk, url)
        return redirect('home_page')

    return render(request, "linkmodifier/edit_qr.html", context)

@login_required
def delete_qr(request, pk):
    link = get_object_or_404(Link, pk=pk)
    context = {'Qr':link}

    if request.method == 'POST':
        if link.png_with_qr:
            link.png_with_qr = None
            link.save()
        folder_dir = "linkmodifier/media/images"
        for qr_code in os.listdir(folder_dir):
            if qr_code == f"QrCode{pk}.png":
                os.remove(folder_dir + '/' + qr_code)
        return redirect('home_page')

    return render(request, "linkmodifier/delete_qr.html", context)

@login_required
def add_shortened_link(request,pk):
    links = Link.objects.filter(id=pk).values()

    if request.method=='POST':
        link_obj = Link.objects.get(id=pk)
        slug = ''.join(random.choice(string.ascii_letters) for x in range(10))
        short_url = f"{get_current_site(request)}{reverse('short_redirect', args=[slug])}"
        link_obj.shortened_link = short_url
        link_obj.save()
        return redirect('home_page')

    context = {'links': links}
    return render(request, "linkmodifier/add_shortened_link.html", context)

def shortened_link_redirect(request, slugs):
    short_url = f"{get_current_site(request)}/{slugs}/"
    link_obj = Link.objects.get(shortened_link=short_url)
    return redirect(link_obj.url_link)

@login_required
def delete_shortened_link(request, pk):
    link_obj = get_object_or_404(Link, pk=pk)
    if request.method=='POST':
        if link_obj.shortened_link:
            link_obj.shortened_link = None
            link_obj.save()
        return redirect('home_page')
    context = {'short_link':link_obj.shortened_link}
    return render(request, "linkmodifier/delete_shortened_link.html", context)




