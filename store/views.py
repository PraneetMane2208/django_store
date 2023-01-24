from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product,Collection
from .serializers import productSerializer,CollectionSerializer
from django.db.models.aggregates import Count

# def product_list(request):
#     return HttpResponse('ok')


class ProductList(APIView):
    def get(self,request):
        queryset=Product.objects.select_related('collection').all()
        serializer=productSerializer(queryset,many=True,context={'request':request})
        return Response(serializer.data)

    def post(self,request):
        serializer=productSerializer(data=request.data) # LINE 20 IS INITIALIZED TO CREATE PRODUCT
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method=='GET':
#         queryset=Product.objects.select_related('collection').all()
#         serializer=productSerializer(queryset,many=True,context={'request':request})

#         # we have set many=True bcz iterate and we want to convert each product obj to dictionary
#         return Response(serializer.data)
#     elif request.method=='POST':
#         serializer=productSerializer(data=request.data) # LINE 20 IS INITIALIZED TO CREATE PRODUCT
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
        
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
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
    elif(request.method=="DELETE"):
        if product.orderitems.count()>0:
            return Response({'error':'Product item cnt be deleted bcz it is related with other models'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection=get_object_or_404(Collection.objects.annotate(products_count=Count('products')
    ),pk=pk)
    if(request.method=="GET"):
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    elif(request.method=="PUT"):
        serializer=productSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif(request.method=="DELETE"):
        if collection.products.count()>0:
             return Response({'error':'collection cannot be deleted'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def collection_list(request):
    if request.method=='GET':
        queryset=Collection.objects.annotate(products_count=Count('products')).all()
        serializer=CollectionSerializer(queryset,many=True)

        # we have set many=True bcz iterate and we want to convert each product obj to dictionary
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=CollectionSerializer(data=request.data) # LINE 20 IS INITIALIZED TO CREATE PRODUCT
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)