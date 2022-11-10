from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from django.http import HttpResponse
from store.models import Product,OrderItem,Order
# Create your views here.
def say_hello(request):
    # try:
    queryset=Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # queryset=Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    # queryset=Product.objects.prefetch_related('promotion').select_related('collection').all()
    #queryset=Product.objects.filter(unit_price__lt=20).filter(inventory__lt=10)
    # queryset=Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # queryset=Product.objects.filter(title__icontains='coffee')
    # product=Product.objects.order_by('unit_price')  # IT RETURNS PRODUCT DIRECTLY
    # product=Product.objects.latest('unit_price') # IT RETURNS HIGHEST PRICE OBJECT IN DESC
    # exists=Product.objects.filter(pk=1).exists()
    # 1) for product in query_set:
    #     print(product)
    # # return HttpResponse('Hello World')

    # 2) list(query_set)
    # 3)queryset[0:]
    # except ObjectDoesNotExist:
    #     pass

    return render(request,'hello.html',{'name' : 'out','orders':list(queryset)})