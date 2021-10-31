from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, resolve_url
from django.views import View
from .models import Cart,Person,Product,OrderPlaced,User
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from app import forms, pdfconvertor
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import speech_recognition
from django.core import serializers
import pyttsx3


# new import
import email
import smtplib
import ssl
import base64
import os
import pathlib

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email import encoders



from pickle import NONE
from fpdf import FPDF 
import datetime

# new import end


@login_required
def delete(request):
    user=request.user
    user.delete()
    return JsonResponse({"res":"renderLogin"})

class InvoiceGenerator():
    '''
    CUSTOMER_ID = str(101) #from DB (current user's ID)
    CUSTOMER = "Armaan Agrawal, 9876543210" #Current user (<username>+", "+<contact_no>)
    ADDRESS = "112, Ring Road, Indore, Madhya Pradesh, 452010" #from DB (<house no>+" ("+<landmark>+"), "+<city>+", ("+<state>+"), "+<pincode>)
    DATE_OF_PURCHASE = str(datetime.date.today())
    INVOICE_NUMBER = ''.join(str(datetime.date.today()).split("-")) + str(datetime.datetime.now().strftime("%H%M%S")) + CUSTOMER_ID
    PRODUCT_NAME = "Vivo V20 Pro" #<brand name> + " " + <product name>
    BILLING_AMT = "Rs. "+str(25000) #Final Billing Amount from cart section
    '''
    CUSTOMER_ID = None
    CUSTOMER = None
    ADDRESS = None
    DATE_OF_PURCHASE = None
    INVOICE_NUMBER = None
    PRODUCT_NAME = None
    BILLING_AMT = None

    def set_data(self,userID,username,mob_num,house_num,landmark,city,state,pincode,products,billing_amt):
        self.CUSTOMER_ID = str(userID)
        self.CUSTOMER = username +", " + str(mob_num)
        self.ADDRESS = house_num + " (" + landmark + "), " + city + " (" + state + "), " + str(pincode)
        self.DATE_OF_PURCHASE = str(datetime.date.today())
        self.INVOICE_NUMBER = ''.join(str(datetime.date.today()).split("-")) + str(datetime.datetime.now().strftime("%H%M%S")) + self.CUSTOMER_ID
        self.PRODUCT_NAME = ', '.join(products)
        self.BILLING_AMT = "Rs. " + str(billing_amt)

    def generate_invoice(self):
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", 'BI', size = 40)
        pdf.cell(200, 10, txt = "MobiDuniya", ln = 1, align = 'C')

        pdf.cell(200, 30, txt = " ", ln = 2, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Billed To : ", ln = 3, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.CUSTOMER, ln = 4, align = 'L')
        pdf.cell(50, 8, txt = self.ADDRESS, ln = 5, align = 'L')

        pdf.cell(200, 10, txt = " ", ln = 6, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Date of Purchase : ", ln = 7, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.DATE_OF_PURCHASE, ln = 8, align = 'L')

        pdf.cell(200, 10, txt = " ", ln = 9, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Product : ", ln = 10, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.PRODUCT_NAME, ln = 11, align = 'L')

        pdf.cell(200, 10, txt = " ", ln = 12, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Billing Amount : ", ln = 13, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.BILLING_AMT, ln = 14, align = 'L')

        pdf.cell(200, 10, txt = " ", ln = 15, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Invoice Number : ", ln = 16, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.INVOICE_NUMBER, ln = 17, align = 'L')

        pdf.output("MobiDuniya-Invoice-"+self.INVOICE_NUMBER+".pdf")

        return "MobiDuniya-Invoice-"+self.INVOICE_NUMBER+".pdf"




class MailAssistant():
    
    sender_email = "mobiduniya2021"
    sender_password = "Mobi@2021#Duniya"
    reciever_email = ""
    body = ""
    subject = ""
    
    def __addAttachments(self,pdf_file):
        
        path = pdf_file
        fileName = os.path.basename(path)
        File = MIMEApplication(open(path, 'rb').read())
        File.add_header('Content-Disposition', 'attachment', filename=fileName)
        return File

    def __emailSkeleton(self,pdf_file):
        message = MIMEMultipart()

        message['From'] = self.sender_email
        message['To'] = self.reciever_email
        message['Subject'] = self.subject
        
        message.attach(MIMEText(self.body, "plain"))
        message.attach(self.__addAttachments(pdf_file))
        
        return message.as_string()

    def __sendMail(self,message):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        
        if self.reciever_email != "" and message != "":
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.reciever_email, message)
            server.close()
            return True
        else:
        	server.close()
        	return False

    def sendInvoice(self,ps,ls,final_bill):
        ig = InvoiceGenerator() 
        ig.set_data(userID=ps[0],
                    username=ps[1],
                    mob_num=ps[2],
                    house_num=ps[3],
                    landmark=ps[4],
                    city=ps[5],
                    state=ps[6],
                    pincode=ps[7],
                    products=ls,
                    billing_amt= final_bill )
        invoice = ig.generate_invoice()
        #self.reciever_email = userID.email

        self.reciever_email = ps[8]
        self.subject = "Invoice of Purchase"
        self.body = "Thank you for making a purchase from MobiDuniya"
        message = self.__emailSkeleton(invoice)
        sent= self.__sendMail(message)
        if os.path.isfile(invoice):
            os.remove(invoice)
        return sent    







# output audio
def outputAudio(output_text):
    engine=pyttsx3.init("sapi5")
    voices=engine.getProperty("voices")
    engine.setProperty("voice",voices[1].id)
    engine.setProperty("volume",1.0)
    engine.setProperty("rate",200)
    engine.say(output_text)
    engine.runAndWait()
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
@login_required
def compare(request):
    return render(request,'app/compare.html')

@login_required
def productviewcompare(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'app/productviewcompare.html',{'productt':product})

def suggestion(request):
    productData = Product.objects.all()
    ram = set()
    rom = set()
    processor = set()
    display = set()
    front = set()
    rear = set()
    responseData = dict()
    for x in productData:
        ram.add(x.ram)
        rom.add(x.internal) 
        processor.add(x.processor)
        display.add(x.display)
        front.add(x.front_camera)
        rear.add(x.rear_camera)

    # print(ram)
    responseData['ram'] = list(ram) 
    responseData['internal'] = list(rom) 
    responseData['processor'] = list(processor) 
    responseData['display'] = list(display) 
    responseData['frontCamera'] = list(front) 
    responseData['rearCamera'] = list(rear) 
    # print(responseData)
    return render(request,'app/suggestion.html',{'data':responseData})

def suggestphone(request):
    # True represents that following brands have been checked
    SAMSUNG = request.GET['samsung']   
    OPPO = request.GET['oppo']
    VIVO = request.GET['vivo']
    ONEPLUS = request.GET['oneplus']
    XIAOMI = request.GET['xiaomi']
    REALME = request.GET['realme']

    brand_list = [
         ['samsung',SAMSUNG],
         ['oppo',OPPO],
         ['vivo',VIVO],
         ['oneplus',ONEPLUS],
         ['xiaomi',XIAOMI],
         ['realme',REALME],
         ] 

    ###### Assumed that user wants only xiaomi and realme mobiles
    #This is just assumed one, replace with data coming from input field of form
    PRICE_RANGE = request.GET['price']
    RAM = int(request.GET['ram'])
    STORAGE = int(request.GET['internal'])
    PROCESSOR = request.GET['processor']
    DISPLAY = request.GET['display']
    R_CAM = int(request.GET['rear_camera'])
    F_CAM = int(request.GET['front_camera'])

    # print(SAMSUNG,OPPO,VIVO,ONEPLUS,XIAOMI,REALME,PRICE_RANGE,RAM,STORAGE,PROCESSOR,DISPLAY,R_CAM,F_CAM)
    # print(type(R_CAM))
    # print(type(RAM))


    #adjusting price as per value set
    min_price = -1
    max_price = -1
    if PRICE_RANGE == "< 15000":
        min_price = 0
        max_price = 15000
    elif PRICE_RANGE == "15000-20000":
        min_price = 15000
        max_price = 20000
    elif PRICE_RANGE == "20000-25000":
        min_price = 20000
        max_price = 25000
    elif PRICE_RANGE == "25000-30000":
        min_price = 25000
        max_price = 30000
    elif PRICE_RANGE == "> 30000":
        min_price = 30000
        max_price = 20000

    #Query to fetch all mobiles of selected brands and convert it into dictionary where key=<brand + mobile> OR <product ID> & value=0
    ###### Since only realme and xiaomi were checked(as assumed), creating demo dictionary
    
    products = dict()
     
    for x in brand_list:
        if x[1] == 'true':  
            productName = Product.objects.filter(brand = x[0])
            ls = [] 
            for x in productName:
                product_id = x.id
                brand = x.brand
                title = x.title
                price = x.selling_price
                display = x.display
                ram  = x.ram
                internal = x.internal
                processor = x.processor
                front_camera = x.front_camera.split(' ')[0]
                rear_camera = x.rear_camera.split(' ')[0]
                if price >= min_price and price <= max_price:
                    products[brand+title] = {'value':0,"id":product_id,'brand':brand,'title':title,'price':price,'ram':int(ram),'internal':int(internal),'display':display,'processor':processor,'front_camera':int(front_camera),'rear_camera':int(rear_camera)}   
            

    
    # # print('products',products)
    # print('access',products['samsungGalaxy A52s 5G']['price'] )
    # products = {"xiaomi mi 10i":0,
    #             "xiaomi note 10s":0,
    #             "xiaomi note 10 pro max":0,
    #             "xiaomi mi 11 lite":0,
    #             "xiaomi mi 11x pro 5g":0,
    #             "xiaomi redmi 9 power":0,
    #             "xiaomi mi 11x":0,
    #             "realme x7 max 5g":0,
    #             "realme gt master edition":0,
    #             "realme 8":0,
    #             "realme x3 superzoom":0,
    #             "realme x7 5g":0,
    #             "realme 8 pro":0}
    

    for key,value in products.items():
        if min_price <= products[key]['price'] < max_price:
            products[key]['value'] += 1
        if products[key]['ram'] >= RAM:
            products[key]['value'] += 1
        if products[key]['internal'] >= STORAGE:
            products[key]['value'] += 1
        if PROCESSOR in products[key]['processor']:
            products[key]['value'] += 1
        if DISPLAY in products[key]['display']:
            products[key]['value'] += 1
        if products[key]['rear_camera'] >= R_CAM:
            products[key]['value'] += 1
        if products[key]['front_camera'] >= F_CAM:
            products[key]['value'] += 1
    
    # print('res',products)
    ls = []
    for key,value in products.items():
          ls.append(products[key]['value'])

    max_val = max(ls)
    # print('max',max_val);    
        
    res = {key:val for key,val in products.items() if val['value'] == max_val}
    
    # print(res)

    msg = "No Mobile available" 
    if(len(res)>1):
        lowest_cost = 500000
        lowest_cost_set = None
        for key,value in res.items():
            if res[key]['price'] < lowest_cost:
                lowest_cost = res[key]['price']
                lowest_cost_set = [ res[key]['id'],key ]     
        return JsonResponse({'responseData':lowest_cost_set}) 
    else:
        return JsonResponse({'responseData':['',msg] })
    
   
    





@login_required
def getproduct(request):
    if request.method == 'GET':
        brand_name=request.GET['brandName']
        data = Product.objects.filter(brand=brand_name)
        ls = []
        for x in data:
             ls.append([x.id,x.title])
        responsedata = ls    
        return JsonResponse({"responsedata":responsedata})

@login_required
def getfeatures(request):
    productId_1 = request.GET['product_id_1']
    productId_2 = request.GET['product_id_2']
    ls1 = []
    print(productId_1,productId_2)
    productData1 = Product.objects.filter(id = productId_1)
    productData2 = Product.objects.filter(id = productId_2)
    for x,y in zip(productData1,productData2):
        ls1.append([x.brand,y.brand])
        ls1.append([x.title,y.title])
        ls1.append([x.selling_price,y.selling_price])
        ls1.append([x.body_length,y.body_length])
        ls1.append([x.body_width,y.body_width])
        ls1.append([x.body_weight,y.body_weight])
        ls1.append([x.battery,y.battery])
        ls1.append([x.display,y.display])
        ls1.append([x.resolution,y.resolution])
        ls1.append([x.screen_to_body_ratio,y.screen_to_body_ratio])
        ls1.append([x.refresh_rate,y.refresh_rate])
        ls1.append([x.processor,y.processor])
        ls1.append([x.ram,y.ram])
        ls1.append([x.internal,y.internal])
        ls1.append([x.rear_camera,y.rear_camera])
        ls1.append([x.front_camera,y.front_camera])
        ls1.append([x.os,y.os])



                      
    # print(list(productData2)) 
    return JsonResponse({
        "productId_1":productId_1,
        "productId_2":productId_2,
        "productData":ls1      
    }) 

def compareshowproducts(request):
    if request.method == 'GET':
        id=request.GET['id']
        data = Product.objects.filter(id=id)
        ls = []
        
        for x in data:
            ls.append(x.selling_price)
            ls.append(x.battery)
            ls.append(x.ram)
            ls.append(x.rear_camera)
            ls.append(x.front_camera)
            ls.append(str(x.product_image1))
            ls.append(str(x.product_image2))
            ls.append(str(x.product_image3))
            ls.append(str(x.product_image4))
            ls.append(str(x.product_image5))

        print(ls)    
            
        return JsonResponse({"responseData":ls} )



class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)  
        if form.is_valid():
            # messages.success(request,'Congratulations!! Registered Successfully')
            outputAudio("Registered Successfully") 
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
    person=Person.objects.filter(id=custid)

    ls = [] 

    for c in cart:
        print(c.product)
        cc = str(c.product) 
        print(type(cc)) 
        pid = int(cc)
        # pid = c.product.id 
        # print('--',pid) 
        productData = Product.objects.filter(id = pid)
        for x in productData:
            ls.append(x.title)

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

            print('totalaMount',totalamount)
            

    for c in cart:
        OrderPlaced(user=user,person=customer,product=c.product,quantity=c.quantity).save()   
        c.delete()
    
    ps=[]
    for p in person:
        ps.append(p.id)
        ps.append(p.name)
        ps.append(p.phone_no)
        ps.append(p.house_no)
        ps.append(p.landmark)
        ps.append(p.city)
        ps.append(p.state)
        ps.append(p.zipcode)
        ps.append(p.email)

        




    ma = MailAssistant()
    ma.sendInvoice(ps,ls,totalamount)

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
            outputAudio("Profile Updated Successfully") 
            return redirect('/')

        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'}) 

def dashboard(request):
    user=request.user
    per=Person.objects.get(user=user)
    outputAudio("Welcome to the Dashboard")
    return render(request,'app/user.html',{'person':per}); 

@login_required
def searchbox(request):
    user = request.user
    reqtext = request.GET['text'] 
    ls = reqtext.split(" ")
    newls = []
    for x in ls:
        if x == "5g" or x== "5G":
            newls.append("5G")
        else:
            newls.append(x.capitalize())
    
    text = " ".join(newls)
                        
    # text = reqtext.capitalize()
    mobile_query = False

    print('hee',text)
    
    #Query to fetch all brand name and convert it into "list(set(QUERY))"
    #Creating demo list for working purpose
    brands = ["Samsung","Oppo","Vivo","Xiaomi","Oneplus","Realme"]
    # for index,item in enumerate(brands):
    #     brands[index] = item.lower().replace(" ","")
    
    for brand_index,brand in enumerate(brands):
        if brand in text:

            product_matched = False
            brand = brand.lower()  
            #Query to fetch all products of particular brand name and convert it into "list(set(QUERY))"
            #Assuming brand=samsung gets matched, hence product list will now be like

            productData=Product.objects.filter(brand = brand)
            products = []
            for x in productData:
                products.append(x.title) 

            print(products)  
                                        
            temp_products = ['']*len(products)
            
            # for index,item in enumerate(products):
            #     temp_products[index] = item.capitalize()

            # print(temp_products)


            # for index,item in enumerate(temp_products):
            #     if item[-2:] == '5g':
            #         temp_products[index] = item[:-2]
             
            for product_index,product in enumerate(products):

                if product in text:
                    product_matched = True
                    mobile_query = True

                    if "Buy" in text or "Purchase" in text:
                        #Directly add the product in cart -> brand = <brand> & mobileName = <products[product_index]>
                        #Redirect to Cart
                        p_id = 0
                        prodData = Product.objects.filter(title = product)
                        for x in prodData:
                            p_id = x.id    
                        product=Product.objects.get(id=p_id)
                        Cart(user=user,product=product).save()
                        print('id',p_id)
                        return JsonResponse({"resData":"render_cart"})
                    else:
                        #Fetch the id of mobile where mobileName = <products[product_index]> 
                        #Redirect to product view page where product ID = fetched one
                        p_id = 0
                        prodData = Product.objects.filter(title = product)
                        for x in prodData:
                            p_id = x.id    
                        print('id',p_id)
                        return JsonResponse({"productId":p_id})
                

            if not product_matched:
                #Redirect to web page which comes from dropdown where Brand = <brand>
                mobile_query = True
                for x in brands:
                    if x in text:
                        if x == "xiaomi" or "Xiaomi":
                            return JsonResponse({"brandName":"mi"})
                        else:
                            return JsonResponse({"brandName":x})

                            
            
                
                

        
    if not mobile_query:
        
        if "Dashboard" in text or "Profile" in text:
            #Redirect to UserProfile section
            return JsonResponse({"user":"userProfile"})

        elif "Cart" in text or "Kart" in text:
            #Redirect to Cart page
            return JsonResponse({"cart":"userCart"})


        elif "Compare" in text:
            #Redirect to Mobile Comparison page
            return JsonResponse({"compare":"userCompare"})


        elif "Suggest" in text:
            #Redirect to Mobile Suggestion page
            return JsonResponse({"suggest":"userSuggest"})

        elif "Password" in text:
            #Redirect to Change Password page
            return JsonResponse({"password":"userPassword"})
        elif "Home" in text:
            return JsonResponse({"home":"userHome"})

    #     elif "delete" in text:
    #         #Query to delete account
    #         #Redirect to Index page
    #         pass

        elif "Log Out" in text or "Sign Out" in text or "Sign Me Out" in text:
            return JsonResponse({"logout":"userLogout"})
        else:
            return JsonResponse({"default":"userDefault"}) 

# @login_required
# def delete_user(request):
#     if request.method=='POST':
#         usr=request.user
#         usr.delete()
#     return redirect('/accounts/login')


