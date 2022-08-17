from django.contrib import admin
from .models import *
# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    list_display= ('id','image_tag','alt_txt')
admin.site.register(Banners,BannerAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','image_tag','title']
admin.site.register(Category,CategoryAdmin)

class SizeAdmin(admin.ModelAdmin):
    list_display=['id','title','alt_txt']
admin.site.register(Size,SizeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','image_tag','title','category','spec','status','is_featured']
    list_editable=['is_featured']
admin.site.register(Product,ProductAdmin)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=['id','product','category','size','price']
admin.site.register(ProductAttribute,ProductAttributeAdmin)
    
    