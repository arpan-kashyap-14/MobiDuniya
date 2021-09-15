from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.deletion import CASCADE

STATE_CHOICES=(
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Andra Pradesh','Andra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman & Diu','Daman & Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujrat','Gujrat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttarakhand','Uttarakhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),

)

CARD_CHOICES =(
    ('master','master'),
    ('visa','visa'),
    ('credit card','credit card'),
    ('debit card','debit card'),
)


# Create your models here.

class Person(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    email=models.EmailField(max_length=50)
    name=models.CharField(max_length=30)
    phone_no=models.CharField(max_length=10)
    customer_image=models.ImageField(upload_to='productimg')
    landmark=models.CharField(max_length=25)
    city=models.CharField(max_length=20)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)
    is_seller=models.BooleanField()
    email_verified=models.BooleanField()
    phone_no_verified=models.BooleanField()
    card_type=models.CharField(choices=CARD_CHOICES,max_length=20)
    card_no=models.CharField(max_length=16)
    card_holder=models.CharField(max_length=30)
    valid_from=models.DateField()
    valid_through=models.DateField()


    def __str__(self):
        return str(self.id)

BRAND_CHOICES=(
    ('samsung','samsung'),
    ('oppo','oppo'),
    ('vivo','vivo'),
    ('mi','mi'),
    ('realme','realme'),
    ('oneplus','oneplus'),   
)        


class Product(models.Model):
    title=models.CharField(max_length=50)
    selling_price=models.FloatField()
    brand=models.CharField(max_length=10,choices=BRAND_CHOICES)
    product_image1=models.ImageField(upload_to='productimg',blank=True,null=True)
    product_image2=models.ImageField(upload_to='productimg',blank=True,null=True)
    product_image3=models.ImageField(upload_to='productimg',blank=True,null=True)
    product_image4=models.ImageField(upload_to='productimg',blank=True,null=True)
    product_image5=models.ImageField(upload_to='productimg',blank=True,null=True)
    processor=models.CharField(max_length=25,blank=True)
    battery=models.CharField(max_length=25,blank=True)
    ram=models.CharField(max_length=5,blank=True)
    internal=models.CharField(max_length=5,blank=True)
    expandable=models.CharField(max_length=5,blank=True)
    display=models.CharField(max_length=15,blank=True)
    resolution=models.CharField(max_length=15,blank=True)
    body_length=models.CharField(max_length=5,blank=True)
    body_width=models.CharField(max_length=5,blank=True)
    screen_to_body_ratio=models.CharField(max_length=5,blank=True)
    body_weight=models.CharField(max_length=5,blank=True)
    refresh_rate=models.CharField(max_length=15,blank=True)
    front_camera=models.CharField(max_length=5,blank=True)
    rear_camera=models.CharField(max_length=5,blank=True)
    bluetooth=models.CharField(max_length=15,blank=True)
    sim_support=models.CharField(max_length=25,blank=True)
    usb=models.CharField(max_length=10,blank=True)
    earphone=models.CharField(max_length=10,blank=True)
    microphone=models.CharField(max_length=10,blank=True)
    sensors=models.CharField(max_length=50,blank=True)
    os=models.CharField(max_length=25,blank=True)
    available=models.BooleanField()


    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    person=models.ForeignKey(Person,on_delete=CASCADE)
    product=models.ForeignKey(Product,on_delete=CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')        
        
