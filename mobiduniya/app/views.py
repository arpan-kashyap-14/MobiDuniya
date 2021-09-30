from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Cart,Person,Product,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from app import forms
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        samsung=Product.objects.filter(brand='samsung')
        oppo=Product.objects.filter(brand='oppo')
        vivo=Product.objects.filter(brand='vivo')
        mi=Product.objects.filter(brand='xiaomi')
        realme=Product.objects.filter(brand='realme')
        oneplus=Product.objects.filter(brand='oneplus')
        return render(request,'app/home.html',{'samsung':samsung,'oppo':oppo,'vivo':vivo,'mi':mi,'realme':realme,'oneplus':oneplus})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetaill.html',{'productt':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user) 
        amount=0.0
        shipping_amount=0.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.selling_price)
                amount += tempamount
            if amount == 0:
                shipping_amount = 0.0
            else:
                shipping_amount = 70.0 
                     
            print(shipping_amount) 
            print(amount)  
            totalamount=amount + (shipping_amount)   
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'shipping_amount':shipping_amount})    
        else:
            return render(request,'app/emptycart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0 
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.selling_price)
            amount+=tempamount
        data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount
        
            }
        return JsonResponse(data)


def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity > 1:
            c.quantity -= 1
        c.save()
        amount=0.0
        shipping_amount=70.0 
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.selling_price)
            amount+=tempamount
        data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount
        
            }
        return JsonResponse(data)


def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.selling_price)
            amount+=tempamount

        if amount == 0:
            shipping_amount = 0.0 
        else:
            shipping_amount = 70.0

        print(shipping_amount)     

        data={
                'amount':amount,
                'totalamount':amount+shipping_amount,
                'shipping_amount':shipping_amount
        
            }
        return JsonResponse(data)




# def profile(request):
#  return render(request, 'app/profile.html')
@login_required
def address(request):
    add=Person.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

@login_required
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
        mi=Product.objects.filter(brand='xiaomi')
    elif data=='below':
        mi=Product.objects.filter(brand='xiaomi').filter(selling_price__lt=20000)
    elif data=='above':
        mi=Product.objects.filter(brand='xiaomi').filter(selling_price__gt=20000)    

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
        form = CustomerRegistrationForm(request.POST)  
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
            return redirect('/accounts/login/') 
              
        return render(request,'app/customerregistration.html',{'form':form})
          

# def signup(request):
#     return render(request,'app/customerregistration.html')    
                
         

@login_required
def checkout(request):
    user=request.user
    add=Person.objects.filter(user=user)
    cart_item=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.selling_price)
            amount+=tempamount
        totalamount=amount+shipping_amount    



    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_item':cart_item})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Person.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,person=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")    

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        usr=request.user
        form=CustomerProfileForm(request.POST,request.FILES)
        if form.is_valid():
            id = request.user.id  
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            phone_no=form.cleaned_data['phone_no']
            customer_image=form.cleaned_data['customer_image']
            house_no=form.cleaned_data['house_no']
            landmark=form.cleaned_data['landmark']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            # card_no=form.cleaned_data['card_no']
            # card_type=form.cleaned_data['card_type']
            # card_holder=form.cleaned_data['card_holder']
            # valid_from=form.cleaned_data['valid_from']
            # valid_through=form.cleaned_data['valid_through'] 

    
            obj = Person(id=id,user=usr,name=name,email=email,phone_no=phone_no,customer_image=customer_image,

                     house_no=house_no,landmark=landmark,city=city,state=state,zipcode=zipcode)

            obj.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')

        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'}) 

def dashboard(request):
    user=request.user

    per=Person.objects.get(user=user)
    return render(request,'app/user.html',{'person':per}); 


# def getDashboard(request):
#     JsonResponse(data)
    
