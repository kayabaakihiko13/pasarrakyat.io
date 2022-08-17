from .models import Product, ProductAttribute


def get_filters(request):
    cats=Product.objects.distinct().values('category__title','category__id')
    sizes=ProductAttribute.objects.distinct().values('size_title','size__id')
    
    data={'cats':cats,'sizes':sizes}
    return data