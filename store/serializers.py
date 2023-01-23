from rest_framework import serializers
from store.models import Product,Collection
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']
    # id=serializers.IntegerField()
    # title=serializers.CharField(max_length=250)


class productSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        # fields='__all__'  # It is bad practise we dont want to display all internal
                               # information to external users
        fields=['id','title','price','price_with_tax','collection']
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