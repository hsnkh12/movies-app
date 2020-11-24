from django.shortcuts import render,redirect
from .models import sections,all,user_watchlist_child,user_watchlist_parent,actors
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse,reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import json

def home(request):
    global type
    type="movie"
    if request.user.is_authenticated:
        Li = True
    else:
        Li=False
    return render(request,"menu.html",{"sections":sections.objects.all(),"Li":Li,"name":request.user.username})

def choice_(request):
    data = json.loads(request.body)
    global type
    type = data["card_name"]
    return JsonResponse("choice have been choosed",safe=False)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:    
        if request.method=="POST":
            un = request.POST.get("username")
            ps = request.POST.get("password")
            user = authenticate(request,username=un,password=ps)
            if user is not None:
                login(request,user)
                if user_watchlist_parent.objects.filter(user=request.user).exists():
                    return redirect("home")
                else:   
                    user_watchlist_parent.objects.create(user=request.user)
                    return redirect("home")
            else:
                messages.info(request,'Invalid username or password , Try again')    


        return render(request,"login.html")


def logoutuser(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:    
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account is created for '+user)
                return redirect("login")    

    return render(request,"register.html",{"form":form , "errors":form.errors})

def display(request,section):
    if type !="movie" and type!="series":
        t = "movie"
    else:
        t=type    
    if request.user.is_authenticated:
        Li = True
    else:
        Li=False
    cards=all.objects.filter(section__name=section , type=t ).order_by("rate").reverse
    if request.user.is_authenticated:
        wl = [x.d.name for x in user_watchlist_child.objects.filter(u=user_watchlist_parent.objects.get(user=request.user))]
    else:
        wl=[]    
    print(t)
    return render(request,"section.html",{"cards":cards,"Li":Li,"wl":wl })    


@login_required(login_url="login")
def watchlist(request):
    cards=user_watchlist_child.objects.filter(u=user_watchlist_parent.objects.get(user=request.user))
    if cards.count()==0:
        re = True
    else:
        re=False    
    return render(request,"watchlist.html",{"cards":cards,"re":re})


@login_required(login_url="login")
def add_watchlist(request):
    data = json.loads(request.body)
    card_name = data["card_name"]
    hold = all.objects.get(name=card_name)
    user_watchlist_child.objects.create(d = hold , u =user_watchlist_parent.objects.get(user=request.user) , watchcheck=False)
    return JsonResponse("item was added ",safe=False)

@login_required(login_url="login")
def add_watchlist2(request,name):
    hold = all.objects.get(name=name)
    user_watchlist_child.objects.create(d = hold , u =user_watchlist_parent.objects.get(user=request.user) , watchcheck=False)
    return redirect("home")


@login_required(login_url="login")
def remove_watchlist(request):
    data = json.loads(request.body)
    card_name = data["card_name"]
    r = user_watchlist_child.objects.get(id=int(card_name))
    user_watchlist_child.delete(r)
    return JsonResponse("item has been removed ",safe=False)

def check_watch(request):
    data = json.loads(request.body)
    card_name = data["card_name"]
    r = user_watchlist_child.objects.get(id=card_name)
    if r.watchcheck==True:
        r.watchcheck=False
    else:
        r.watchcheck=True
    r.save()    
    return JsonResponse("item has been removed ",safe=False)      


def read_more(request,name):
    if request.user.is_authenticated:
        Li = True
    else:
        Li=False
    pointed = all.objects.get(name=name)
    cast = actors.objects.filter(roles__name=name)
    if request.user.is_authenticated:
        wl = [x.d.name for x in user_watchlist_child.objects.filter(u=user_watchlist_parent.objects.get(user=request.user))]
    else:
        wl=[]   
    return render(request,"movie.html",{"pointed":pointed,"cast":cast,"Li":Li,"wl":wl})    