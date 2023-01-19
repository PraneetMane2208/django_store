from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import productSerializer

# def product_list(request):
#     return HttpResponse('ok')
@api_view()
def product_list(request):
    return Response('ok')

@api_view()
def product_detail(request,id):
    try:
        product=Product.objects.get(pk=id)
        serializer=productSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)