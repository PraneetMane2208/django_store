from django.shortcuts import render
import collections
from django.db import transaction
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F,Func,Value,ExpressionWrapper,DecimalField 
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count,Max,Min,Avg
from django.db.models.functions import Concat
from django.http import HttpResponse
from store.models import Product,OrderItem,Order,Customer,Collection
from tags.models import TaggedItem
# Create your views here.
def say_hello(request):
    with transaction.atomic():

        order=Order()
        order.customer_id=1
        order.save()

        item=OrderItem()
        item.order=order
        item.product_id=1
        item.quantity=1
        item.unit_price=10
        item.save()
    # collection=Collection.objects.get(pk=11)
    # collection.feature_product=None
    # collection.save()

    # Collection.objects.filter(pk=11).update(feature_product=None)

    # collection=Collection()
    # collection.title='Mobile phone'
    # collection.feature_product=Product(pk=1)
    # collection.save()
    # TaggedItem.objects.get_tags_for(Product,1)
    

    # discounted_price=ExpressionWrapper(F('unit_price') *0.8,output_field=DecimalField())
    # queryset=Product.objects.annotate(discounted_price=discounted_price)
    # # try:
    # result=Product.objects.aggregate(count=Count('id'),min_price=Min('unit_price'))
    # queryset=Customer.objects.annotate(
    #     full_name=Func(F('first_name'),Value(' '),F('last_name'),function='CONCAT')
    # )
    # queryset=Customer.objects.annotate(
    #      full_name=Concat('first_name',Value(' '),'last_name')
    #  )

    # queryset=Customer.objects.annotate(
    #      orders_count=Count('order'))

    
    # queryset=Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
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
    # ll = list(queryset)
    # cut = ll[0].full_name
    return render(request,'hello.html',{'name' : 'cut','tags':list(queryset)})