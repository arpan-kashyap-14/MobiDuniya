from django.http import request
from django.shortcuts import render
from django.views import View
from .models import Cart,Person,Product,OrderPlaced
from .forms import CustomerRegistrationForm
from django.contrib import messages
from app import forms

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        samsung=Product.objects.filter(brand='samsung')
        oppo=Product.objects.filter(brand='oppo')
        vivo=Product.objects.filter(brand='vivo')
        mi=Product.objects.filter(brand='mi')
        realme=Product.objects.filter(brand='realme')
        oneplus=Product.objects.filter(brand='oneplus')
        return render(request,'app/home.html',{'samsung':samsung,'oppo':oppo,'vivo':vivo,'mi':mi,'realme':realme,'oneplus':oneplus})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'app/productdetaill.html',{'productt':product})

def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def mobile(request):
 return render(request, 'app/mobile.html')

def samsung(request,data=None):
    if data==None:
        samsung=Product.objects.filter(brand='samsung')
    elif data=='below':
        samsung=Product.objects.filter(brand='samsung').filter(selling_price__lt=20000)
    elif data=='above':
        samsung=Product.objects.filter(brand='samsung').filter(selling_price__gt=20000)    

    return render(request,'app/samsung.html',{'samsung':samsung})

def vivo(request,data=None):
    if data==None:
        vivo=Product.objects.filter(brand='vivo')
    elif data=='below':
        vivo=Product.objects.filter(brand='vivo').filter(selling_price__lt=20000)
    elif data=='above':
        vivo=Product.objects.filter(brand='vivo').filter(selling_price__gt=20000)    

    return render(request,'app/vivo.html',{'vivo':vivo})

def oppo(request,data=None):
    if data==None:
        oppo=Product.objects.filter(brand='oppo')
    elif data=='below':
        oppo=Product.objects.filter(brand='oppo').filter(selling_price__lt=20000)
    elif data=='above':
        oppo=Product.objects.filter(brand='oppo').filter(selling_price__gt=20000)    

    return render(request,'app/oppo.html',{'oppo':oppo})

def mi(request,data=None):
    if data==None:
        mi=Product.objects.filter(brand='mi')
    elif data=='below':
        mi=Product.objects.filter(brand='mi').filter(selling_price__lt=20000)
    elif data=='above':
        mi=Product.objects.filter(brand='mi').filter(selling_price__gt=20000)    

    return render(request,'app/mi.html',{'mi':mi})

def realme(request,data=None):
    if data==None:
        realme=Product.objects.filter(brand='realme')
    elif data=='below':
        realme=Product.objects.filter(brand='realme').filter(selling_price__lt=20000)
    elif data=='above':
        realme=Product.objects.filter(brand='realme').filter(selling_price__gt=20000)    

    return render(request,'app/realme.html',{'realme':realme})

def oneplus(request,data=None):
    if data==None:
        oneplus=Product.objects.filter(brand='oneplus')
    elif data=='below':
        oneplus=Product.objects.filter(brand='oneplus').filter(selling_price__lt=20000)
    elif data=='above':
        oneplus=Product.objects.filter(brand='oneplus').filter(selling_price__gt=20000)    

    return render(request,'app/oneplus.html',{'oneplus':oneplus})


# def login(request):
#  return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})

# def signup(request):
#     return render(request,'app/customerregistration.html')    
                
         


def checkout(request):
 return render(request, 'app/checkout.html')
