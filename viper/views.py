from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from store.models import Product
# Create your views here.
def say_hello(request):
    # try:

    # product=Product.objects.get(pk=1)
    exists=Product.objects.filter(pk=1).exists()
    # 1) for product in query_set:
    #     print(product)
    # # return HttpResponse('Hello World')

    # 2) list(query_set)
    # 3)queryset[0:]
    # except ObjectDoesNotExist:
    #     pass

    return render(request,'hello.html',{'name' : 'out'})