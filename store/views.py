from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import productSerializer,CollectionSerializer

# def product_list(request):
#     return HttpResponse('ok')
@api_view()
def product_list(request):
    queryset=Product.objects.select_related('collection').all()
    serializer=productSerializer(queryset,many=True,context={'request':request})

    # we have set many=True bcz iterate and we want to convert each product obj to dictionary
    return Response(serializer.data)

@api_view()
def product_detail(request,id):
    product=get_object_or_404(Product,pk=id)
    serializer=productSerializer(product)
    return Response(serializer.data)
    
@api_view()
def collection_detail(request,pk):
    collection=get_object_or_404(Collection,pk=pk)
    serializer=CollectionSerializer(collection)
    return Response(serializer.data)
    