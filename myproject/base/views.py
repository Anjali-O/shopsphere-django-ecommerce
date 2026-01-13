from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        cartproducts_count = CartModel.objects.filter(host=request.user).count()

    else:
        cartproducts_count=False
    nomatch=False
    trend=False
    offer=False
    if 'q' in request.GET:
        q=request.GET['q']
        all_data=Products.objects.filter(Q(pname__icontains=q)|Q(pdesc__icontains=q))
        print(len(all_data))
        if len(all_data)==0:
            nomatch=True

    
    elif 'cat' in request.GET:
           cat=request.GET['cat']
           all_data=Products.objects.filter(pcategory=cat)

    elif 'trending' in request.GET:
        all_data=Products.objects.filter(trending=True)
        trend=True

    elif 'offer' in request.GET:
        all_data=Products.objects.filter(offer=True)
        offer=True

    else:
        all_data=Products.objects.all()
    category=[]
    for i in Products.objects.all():
        if i.pcategory not in category:
            category+=[i.pcategory]

    return render(request,'home.html',{'data':all_data,'nomatch':nomatch,'category':category,'cartproducts_count':cartproducts_count,'trend':trend,'offer':offer})

def addtocart(request,pk):
    if request.user.is_authenticated:

        product=Products.objects.get(id=pk)
        try:
            cp=CartModel.objects.get(pname=product.pname,host=request.user)
            cp.quantity+=1
            cp.totalprice+=product.price 
            cp.save()
            return redirect('cart')
        except:
            CartModel.objects.create(
            pname=product.pname,
            price=product.price,
            pcategory=product.pcategory,
            quantity=1,
            totalprice=product.price,
            host=request.user

        )
    else:
        return redirect('login_')
    return redirect('cart')


@login_required(login_url='login_')
def cart(request):
    cartproducts_count=CartModel.objects.filter(host=request.user).count()
    cartproducts=CartModel.objects.filter(host=request.user)
    TA=0
    for i in cartproducts:
        TA+=i.totalprice
    return render(request,'cart.html',{'data':cartproducts,'TA':TA,'profile_nav':True,'cartproducts_count':cartproducts_count})



def remove(request,pk):
    cartproduct=CartModel.objects.get(id=pk)
    cartproduct.delete()
    return redirect('cart')


def details(request,pk):
    if request.user.is_authenticated:

        u=Products.objects.get(id=pk)
        cartproducts_count=CartModel.objects.filter(host=request.user).count()
    else:
        return redirect('login_')
    return render(request,'details.html',{'data':u,'profile_nav':True,'cartproducts_count':cartproducts_count})

def csub(reuqest,pk):
    cproduct = CartModel.objects.get(id=pk)
    if cproduct.quantity>1:
        cproduct.quantity-=1
        cproduct.totalprice-=cproduct.price
        cproduct.save()
        return redirect('cart')
    else:
        cproduct.delete()
        return redirect('cart')


def cadd(request,pk):
    cproduct=CartModel.objects.get(id=pk)
    cproduct.quantity+=1
    cproduct.totalprice+=cproduct.price 
    cproduct.save()
    return redirect('cart')


def support(request):
    cartproducts_count=CartModel.objects.filter(host=request.user).count()
    return render(request,'support.html',{'profile_nav':True,'login_nav':True,'cartproducts_count':cartproducts_count})

def knowus(request):
    cartproducts_count=CartModel.objects.filter(host=request.user).count()
    return render(request,'knowus.html',{'profile_nav':True,'login_nav':True,'cartproducts_count':cartproducts_count})


def payment(request):
    cartproducts_count=CartModel.objects.filter(host=request.user).count()
    return render(request,'payment.html',{'cartproducts_count':cartproducts_count,'profile_nav':True})