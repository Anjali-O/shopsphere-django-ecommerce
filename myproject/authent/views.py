from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from base.models import *

# Create your views here.
def login_(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        u=authenticate(username=username,password=password)   
        if u:
            login(request,u) 
            return redirect('home')
        else:
            return render(request,'login_.html',{'status':'wrong password or username'})
    return render(request,'login_.html',{'login_nav':True})

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        try:
            u=User.objects.get(username=username)
            return render(request,'register.html',{'status':'username already existed'})
        except:
            a=User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username
            )
            a.set_password(password)
            a.save()

    return render(request,'register.html',{'login_nav':True})

@login_required(login_url='login_')
def profile(request):
    cartproducts_count=CartModel.objects.filter(host=request.user).count()
    return render(request,'profile.html',{'profile_nav':True,'cartproducts_count':cartproducts_count})

@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect('login_')


def reset(request):
    cartproducts_count=CartModel.objects.filter(host=request.user).count()
    user=request.user
    if request.method=='POST':
        if 'oldpass' in request.POST:
            oldpass=request.POST['oldpass']
            auth_user=authenticate(username=user.username,password=oldpass)
            if auth_user:
                return render(request,'reset.html',{'newpass':True})
            else:
                return render(request,'reset.html',{'wrong':True})
            
    if 'newpass' in request.POST:
        newpass=request.POST['newpass']
        if user.check_password(newpass):
            return render(request,'reset.html',{'same':True})
        user.set_password(newpass)
        user.save()
        return redirect('login_')
    return render(request,'reset.html',{'profile_nav':True,'cartproducts_count':cartproducts_count})

def forgot(request):
    if request.method=='POST':
        username=request.POST.get('username')
        try:
            u=User.objects.get(username=username)
            request.session['fp_user']=u.username
            return redirect('newpassword')
        except User.DoesNotExist:
            return render(request,'forgot.html',{'error':True})

    return render(request,'forgot.html',{'login_nav':True})




def newpassword(request):
    username=request.session['fp_user']
    if username is None:
        return redirect('forgot')
    user=User.objects.get(username=username)
    if request.method=='POST':
        newpass=request.POST.get('newpass')
        if user.check_password(newpass):
            return render(request,'newpassword.html',{'error':True})
        user.set_password(newpass)
        user.save()
        del request.session['fp_user']
        return redirect('login_')
        

    return render(request,'newpassword.html',{'login_nav':True})

    

