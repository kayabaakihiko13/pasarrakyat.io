from django.urls import path
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

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)