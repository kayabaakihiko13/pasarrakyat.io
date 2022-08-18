from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('category-list',views.category_list,name='category-list'),
    path('product-list',views.product_list,name='product-list'),
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category_product_list'),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product-detail'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('load-more-data',views.load_more_data,name='load_more_data'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_list,name='cart'),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    
    # User URL
    path('accounts/signup',views.signup,name='signup'),

    # Checkout
    path('checkout',views.checkout,name='checkout'),
    
    # Paypal Payment
    
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    
    # User Section Start
    path('my_dashboard', views.my_dashboard, name='my_dashboard'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('my_orders_items/<int:id>', views.my_orders_items, name='my_orders_items'),
    
    #My Address
    path('my_addressbook', views.my_addressbook, name='my_addressbook'),
    path('add-address', views.save_address, name='add-address'),
    
    

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)