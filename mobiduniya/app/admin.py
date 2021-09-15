from django.contrib import admin

# Register your models here.
from .models import (
    Person,
    Product,
    Cart,
    OrderPlaced
)
@admin.register(Person)
class PersonModelAdmin(admin.ModelAdmin):
    list_display=['id','user','email','name','phone_no','customer_image','landmark','city','zipcode','state','is_seller','email_verified','phone_no_verified','card_type','card_no','card_holder','valid_from','valid_through']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','brand','product_image1','product_image2','product_image3','product_image4','product_image5',
    'processor','battery','ram','internal','expandable','display','resolution','body_length','body_width','screen_to_body_ratio',
    'body_weight','refresh_rate','front_camera','rear_camera','bluetooth','sim_support','usb','earphone','microphone','sensors','os','available']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','person','product','quantity','ordered_date','status']
