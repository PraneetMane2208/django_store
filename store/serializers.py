from rest_framework import serializers
from store.models import Product,Collection,Review,Cart,CartItem
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','products_count']
    products_count=serializers.IntegerField(read_only='True')
    # id=serializers.IntegerField()
    # title=serializers.CharField(max_length=250)


class productSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        # fields='__all__'  # It is bad practise we dont want to display all internal
                               # information to external users
        fields=['id','title','slug','description','price','inventory','price_with_tax','collection']
    # id=serializers.IntegerField()
    # title=serializers.CharField(max_length=250)
    price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    # collection=serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    # collection=serializers.StringRelatedField()
    # collection=CollectionSerializer()
    # collection=serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='detail'
    # )

    def calculate_tax(self,product):
        return product.unit_price * Decimal(1.5)

   # BOTH MTDS CREATE AND UPDATE IS AUTOMATICALLY CREATED BY DJANGO SO NO NEED TO 
   # OVERWRITE IT
   
    # def create(self, validated_data):
    #     product=Product(**validated_data)  # It unpacks dictionary
    #     product.other=1
    #     product.save()
    #     return product
        
    # def update(self, instance, validated_data):
    #     instance.unit_price=validated_data.get('unit_price')
    #     instance.save()
    #     return instance

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','date','name','description']
    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField()

    
        
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_price']



class CartSerializer(serializers.ModelSerializer):
    
    
    total_price=serializers.SerializerMethodField()
    def get_total_price(self,cart):
        return sum([item.quantity*item.product.unit_price for item in cart.items.all()])
    class Meta:
        model=Cart
        fields=['id','items','total_price']
        # fields=['id','items']
    id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True,read_only=True)

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with this id is found')
        return value

    def save(self, **kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        try:
            #updating an existing item
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance=cart_item
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
            #creating new item
        return self.instance
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']