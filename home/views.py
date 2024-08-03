from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from datetime import datetime
import sweetify
from .forms import RegisterationForm, LoginForm, StayPicsForm, DinePicsForm
from .models import StayPics, DinePics,User
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.decorators import user_passes_test
from BookDetails.models import BookData

def register(req):
    if req.method == 'POST':
        form = RegisterationForm(req.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('login')
    else:
        form = RegisterationForm()
    return render(req, 'regi/register.html', {'form': form})


def user_login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            user = User.objects.get(username = form.cleaned_data['username'])
            if user.check_password(form.cleaned_data['password']):
                login(req, user)
                print(user,'lllllllllllll')
                sweetify.toast(req, 'You have successfully logged in.')
                return redirect('home')
            else:
                sweetify.toast(req, 'Oops, something went wrong!', icon="error", timer=2000)
    else:
        form = LoginForm()
    return render(req, 'regi/login.html', {"form": form})


def user_logout(req):
    logout(req)
    sweetify.toast(req, 'You have successfully logged out.')
    return redirect('login')

def admin_required(func):
    inner = user_passes_test(
        lambda x: x.is_superuser,
    )(func)
    return inner


@admin_required
def stay_pic_edit(req, id):
    edited = StayPics.objects.get(id=id)
    if req.method == 'POST':
        form = StayPicsForm(req.POST, instance=edited)
        if form.is_valid():
            form.save()
            return redirect('stay')
    else:
        form = StayPicsForm(instance=edited)
    return render(req, 'navbar/Stay_pics_edit.html', {'form': form, 'id': id})


def stay_delete(req, id):
    deleting = StayPics.objects.filter(id=id)
    deleting.delete()
    return redirect('stay')


def dinepic(req):
    if req.method == 'POST':
        form = DinePicsForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            return redirect('dine')
    else:
        form = DinePicsForm()
    return render(req, 'navbar/DinePics.html', {'form': form})


def home(req):
    sweetify.success(req, 'Cheers to new toast')
    sweetify.toast(req, 'Cheers to new toast')
    return render(req, 'navbar/home.html')


def stay(request):
    form = None
    show = None
    
    if request.user.is_superuser:
        if request.method == 'POST':
            form = StayPicsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('stay')
        else:
            form = StayPicsForm()
        show = StayPics.objects.all()
    images = StayPics.objects.all()
    context = {
            'form': form,
            'show': show,
            'images': images
        }
    return render(request, 'navbar/stay.html', context)


def dine(req):
    dine_images = DinePics.objects.all()
    return render(req, 'navbar/dine.html', {'dine': dine_images})

@admin_required
def spa(req):
    data = BookData.objects.all() 
    # print(data)
    return render(req, 'navbar/spa.html',{'data':data})


def celebrate(req):  
    return render(req, 'navbar/celebrate.html')

@admin_required
def gallery(req):
    return render(req, 'navbar/gallery.html')

def offers(req):
    return render(req, 'navbar/offers.html')


def url_date(req, id=None):
        today = datetime.today()
        year = today.year
        month = today.month
        return redirect('booking', id=id, year=year, month=month)



