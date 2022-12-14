from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from .models import *
from django.template.loader import render_to_string
from django.db.models.functions import ExtractMonth
from django.db.models import Count
# For User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,AddressBookForm,ProfileForm
from django.contrib.auth import login,authenticate
# checkout
from django.contrib.auth.decorators import login_required

# Paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.


# home views
def home(request):
    banners=Banners.objects.all().order_by('-id')
    data=Product.objects.filter(is_featured=True).order_by('-id') # memnampilkan barang andalan pada halaman home dengan urutan id
    return render(request,'index.html',
                  {
                      'data':data,
                      'banners':banners,
                  }
                  )


# Category_list View
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})



# product_list view
def product_list(request):
    total_data=Product.objects.count()
    data=Product.objects.all().order_by('-id')[:6]
    cats=Product.objects.distinct().values('category__title','category__id') # for choice one of categories with product
    sizes=ProductAttribute.objects.distinct().values('size__title','size__id','price',)
    
    return render(request,'product_list.html',
                  {
                      "data":data,
                      "total_data":total_data,
                      "cats":cats,
                      "sizes":sizes,
                  }
                  )
# Product List Accroding To Category
def category_product_list(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data=Product.objects.filter(category=category).order_by('-id')
    cats=Product.objects.distinct().values('category__title','category__id')
    sizes=ProductAttribute.objects.distinct().values('size__title','size__id')
    
    return render(request,'category_product_list.html',
                  {
                      "data":data,
                      "cats":cats,
                      "sizes":sizes,
                  }
                  )

def product_detail(request,slug,id):
    product=Product.objects.get(id=id)
    releated_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
    sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','price').distinct()
    return render(request,'product_detail.html',{'data':product,'releated':releated_products,'sizes':sizes})

# Search
def search(request):
    q=request.GET['q']
    data=Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request,'search.html',{'data':data})

# Filter Products
# for similary product with same categories
def filter_data(request):
    categories=request.GET.getlist('category[]')
    sizes=request.GET.getlist('size[]')
    allProducts=Product.objects.all().order_by('-id').distinct()
    if len(categories)>0:
        allProducts=allProducts.filter(category__id__in=categories).distinct()
    if len(sizes)>0:
        allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t=render_to_string('ajax/product-list.html',{'data':allProducts})
    return JsonResponse({'data':t})
# Load More    
def load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    data=Product.objects.all().order_by('-id')[offset:offset+limit]
    t=render_to_string('ajax/product-list.html',{'data':data})
    return JsonResponse({'data':t})

# Add to cart
def add_to_cart(request):
	# del request.session['cartdata']
	cart_p={}
	cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
	if 'cartdata' in request.session:
		if str(request.GET['id']) in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cartdata']=cart_data
		else:
			cart_data=request.session['cartdata']
			cart_data.update(cart_p)
			request.session['cartdata']=cart_data
	else:
		request.session['cartdata']=cart_p
	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

# Cart List Page
def cart_list(request):
    # p_id=str(request.GET['id'])
    total_amt=0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
        return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    else:
        return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})
        
# Delete Cart Item
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


# Update Cart Item
def update_cart_item(request):
    p_id=str(request.GET['id'])
    p_qty=request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=p_qty
            request.session['cartdata']=cart_data
        total_amt=0
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
        t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'totalamt':total_amt})
        return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})
# Signup

def signup(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=pwd)
            login(request,user)
    form=SignUpForm
    return render(request,'registration/signup.html',{'form':form})
def success(request):
    return render(request,'success.html')
# Search
@login_required
def checkout(request):
    total_amt=0
    totalAmt=0
    
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            totalAmt+=int(item['qty'])*float(item['price'])
        # Order
        order=CartOrder.objects.create(
            user=request.user,
            total_amt=totalAmt,
            
        )
        # End
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
        # OrderItem
            items=CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-'+str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price']),
            )
        # End
        
    
        # Process Payment
        host=request.get_host()
        paypal_dict={
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':total_amt,
            'item_name':'OrderNo-'+str(order.id),
            'invoice':'INV-'+str(order.id),
            'currency_code':"USD",
            'notify_url':'http://{}{}'.format(host,reverse,('paypal-ipn')),
            'return_url':'http://{}{}'.format(host,reverse,('payment_done')),
            'cancel_url':'http://{}{}'.format(host,reverse,('payment_cancelled')),
            
        }
        form=PayPalPaymentsForm(initial=paypal_dict)
        address=UserAddressBook.objects.filter(user=request.user,status=True).first()
        return render(request,'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'form':form,'address':address})
        
@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')

# User Dashbroad
import calendar
def my_dashboard(request):
    orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber=[]
    totalOrders=[]
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request,'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})
    
# My Order History
def my_orders(request):
    orders=CartOrder.objects.filter(user=request.user).order_by('-id')
    
        
    return render(request,'user/orders.html',{'order':orders}) 

# Order list History
def my_orders_items(request,id):
    order=CartOrder.objects.get(pk=id)
    orders=CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request,'user/orders-items.html',{'order':orders}) 
# Addresss Book
 
def my_addressbook(request):
    addbooks=UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request,'user/addressbok.html',{'addbooks':addbooks}) 

# Save Address
def save_address(request):
    msg=None
    if request.method=='POST':
        form=AddressBookForm(request.POST)
        if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg='Data has Been Saved'
    form=AddressBookForm()
    return render(request,'user/add-address.html',{'form':form})

# Activate address
def activate_address(request):
    a_id=str(request.GET['id'])
    UserAddressBook.objects.update(status=False)
    UserAddressBook.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool':True})


# Edit Profile
def edit_profile(request):
    msg=''
    if request.method=='POST':
        form=ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            msg='Data has Been Saved'
    form=ProfileForm(instance=request.user)
    return render(request,'user/edit-profile.html',{'form':form})


# Save Address
def update_address(request,id):
    address=UserAddressBook.objects.get(pk=id)
    msg=None
    if request.method=='POST':
        form=AddressBookForm(request.POST,instance=address)
        if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg='Data has Been Saved'
    form=AddressBookForm(instance=address)
    return render(request,'user/update-address.html',{'form':form})


