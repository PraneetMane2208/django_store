from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import productSerializer,CollectionSerializer

# def product_list(request):
#     return HttpResponse('ok')
@api_view(['GET','POST'])
def product_list(request):
    if request.method=='GET':
        queryset=Product.objects.select_related('collection').all()
        serializer=productSerializer(queryset,many=True,context={'request':request})

        # we have set many=True bcz iterate and we want to convert each product obj to dictionary
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=productSerializer(data=request.data) # LINE 20 IS INITIALIZED TO CREATE PRODUCT
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PUT'])
def product_detail(request,id):
    product=get_object_or_404(Product,pk=id)
    if(request.method=="GET"):
        serializer=productSerializer(product)
        return Response(serializer.data)
    elif(request.method=="PUT"):
        serializer=productSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)






@api_view()
def collection_detail(request,pk):
    collection=get_object_or_404(Collection,pk=pk)
    serializer=CollectionSerializer(collection)
    return Response(serializer.data)
    