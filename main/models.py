from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
# Create your models here.
class Banners(models.Model):
    image=models.ImageField(upload_to='banner_img/')
    alt_txt=models.CharField(max_length=50)

    class Meta:
        verbose_name_plural='Banner'
        
    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" height="70" />' % (self.image.url))
    
    def __str__(self) :
        return self.alt_txt

class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='cat_imgs')
    
    class Meta:
        verbose_name_plural='1.Category'
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def __str__(self) :
        return self.title

class Size(models.Model):
    title=models.CharField(max_length=20)
    alt_txt=models.CharField(max_length=10)
    
    class Meta:
         verbose_name_plural ='2.Size'
    
    def __str__(self) :
        return self.title
class Product(models.Model):
    STATUS=(
        ('TRUE','Ada'),
        ("FALSE",'Kosong')
    )
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to='product_imgs/')
    slug=models.CharField(max_length=400)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    describe=models.TextField()
    spec=models.CharField(max_length=100)
    nutrition=models.TextField()
    store_instru=models.TextField()
    status=models.CharField(max_length=50,choices=STATUS)
    is_featured=models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural ='3.Products'
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="70" height="50" />'% (self.image.url))
    image_tag.short_description = 'Image'
    
    def __str__(self) :
        return self.title
    
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.FloatField()
    image=models.ImageField(upload_to='product_imgs/',null=True)
    class Meta:
        verbose_name_plural ='4.Products Attribute'

class CartOrder(models.Model):
    paid_choice=(
        ('False','Un Payoff'),
        ('True','Payoff'),
    )
    
    status_choice=(
        ('process','In Process'),
        ('process','Shipped'),
        ('process','Delivered'),
    )
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status=models.CharField(max_length=50,choices=paid_choice,default="False")
    order_dt=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(max_length=50,choices=status_choice,default='process')
    class Meta:
        verbose_name_plural='5.Cart Order'
    
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=200)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()
    
    class Meta:
        verbose_name_plural='6.Cart Order Items'
    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

# My AddresssBook
class UserAddressBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    city=models.CharField(max_length=100)
    street=models.CharField(max_length=200)    
    status=models.BooleanField(default=False)
    class Meta:
        verbose_name_plural='7.Address Book'
    
        
    
    
    
        