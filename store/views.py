from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,ListModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Product,Collection,OrderItem,Review,Cart,CartItem,Customer
from.filters import ProductFilter
from .serializers import productSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,CustomerSerializer
from .pagination import DefaultPagination
from django.db.models.aggregates import Count



class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=productSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields=['title','description']
    ordering_fields=['unit_price','inventory']
    pagination_class=DefaultPagination
    # filterset_fields=['collection_id','unit_price']
    filterset_class=ProductFilter
    # def get_queryset(self):
    #     queryset=Product.objects.all()
    #     collection_id=self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset=queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request':self.request}

    # def delete(self,request,id):
    #     product=get_object_or_404(Product,pk=id)
    #     if product.orderitems.count()>0:
    #         return Response({'error':'Product item cnt be deleted bcz it is related with other models'})
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'Product item cnt be deleted bcz it is related with other models'})
        return super().destroy(request, *args, **kwargs)
    
class CollectionViewSet(ModelViewSet):
    queryset=queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class=CollectionSerializer

    def delete(self,request,pk):
        collection=get_object_or_404(Collection,pk=pk)
        if collection.products.count()>0:
             return Response({'error':'collection cannot be deleted'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer

class CartItemViewSet(ModelViewSet):

    http_method_names=['get','post','patch','delete']
    def get_serializer_class(self):
        if(self.request.method=='POST'):
            return AddCartItemSerializer
        elif(self.request.method=='PATCH'):
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    # serializer_class=CartItemSerializer

    def get_queryset(self):
        return CartItem.objects\
                .filter(cart_id=self.kwargs['cart_pk'])\
                .select_related('product')


class CustomerViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

# class ProductList(ListCreateAPIView):
#     queryset=Product.objects.select_related('collection').all()
#     serializer_class=productSerializer

#     # def get_queryset(self):    # we use this func when there is some logic to generate queryset depend on user
#     #     return Product.objects.select_related('collection').all()
    
#     # def get_serializer_class(self):
#     #     return productSerializer
    
#     def get_serializer_context(self):
#         return {'request':self.request}
    
    

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset=Product.objects.all()
#     serializer_class=productSerializer
#     lookup_field='id'
    
    
#     # def get(self,request,id):
#     #     product=get_object_or_404(Product,pk=id)
        
#     #     serializer=productSerializer(product)
#     #     return Response(serializer.data)
#     # def put(self,request,id):
#     #     product=get_object_or_404(Product,pk=id)
#     #     serializer=productSerializer(product,data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data)

#     def delete(self,request,id):
#         product=get_object_or_404(Product,pk=id)
#         if product.orderitems.count()>0:
#             return Response({'error':'Product item cnt be deleted bcz it is related with other models'})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# # @api_view(['GET','PUT','DELETE'])
# # def product_detail(request,id):
# #     product=get_object_or_404(Product,pk=id)
# #     if(request.method=="GET"):
# #         serializer=productSerializer(product)
# #         return Response(serializer.data)
# #     elif(request.method=="PUT"):
# #         serializer=productSerializer(product,data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         serializer.save()
# #         return Response(serializer.data)
# #     elif(request.method=="DELETE"):
# #         if product.orderitems.count()>0:
# #             return Response({'error':'Product item cnt be deleted bcz it is related with other models'})
# #         product.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset=Collection.objects.annotate(products_count=Count('products'))
#     serializer_class=CollectionSerializer
#     def delete(self,request,pk):
#         collection=get_object_or_404(Collection,pk=pk)
#         if collection.products.count()>0:
#              return Response({'error':'collection cannot be deleted'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    


# @api_view(['GET','PUT','DELETE'])
# def collection_detail(request,pk):
#     collection=get_object_or_404(Collection.objects.annotate(products_count=Count('products')
#     ),pk=pk)
#     if(request.method=="GET"):
#         serializer=CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif(request.method=="PUT"):
#         serializer=productSerializer(collection,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     elif(request.method=="DELETE"):
#         if collection.products.count()>0:
#              return Response({'error':'collection cannot be deleted'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CollectionList(ListCreateAPIView):
#     queryset=Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class=CollectionSerializer

    # def get_queryset(self):
    #     return Collection.objects.annotate(products_count=Count('products')).all()

    # def get_serializer_class(self):
    #     return CollectionSerializer

    # def get(self,request):
    #     queryset=Collection.objects.annotate(products_count=Count('products')).all()
    #     serializer=CollectionSerializer(queryset,many=True)
    #     return Response(serializer.data)
    
    # def post(self,request):
    #     serializer=CollectionSerializer(data=request.data) # LINE 20 IS INITIALIZED TO CREATE PRODUCT
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
        
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)


# @api_view(['GET','POST'])
# def collection_list(request):
#     if request.method=='GET':
#         queryset=Collection.objects.annotate(products_count=Count('products')).all()
#         serializer=CollectionSerializer(queryset,many=True)

#         # we have set many=True bcz iterate and we want to convert each product obj to dictionary
#         return Response(serializer.data)
#     elif request.method=='POST':
#         serializer=CollectionSerializer(data=request.data) # LINE 20 IS INITIALIZED TO CREATE PRODUCT
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
        
#         return Response(serializer.data,status=status.HTTP_201_CREATED)