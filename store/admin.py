from django.db.models.aggregates import Count
from django.contrib import admin

from django.urls import reverse
from django.utils.html import format_html,urlencode
from . import models
from store.models import Order,OrderItem,Customer

from django.db.models import Q,F,Func,Value,ExpressionWrapper,DecimalField 
from django.db.models.functions import Concat

class InventoryFilter(admin.SimpleListFilter):
    title='Inventory'
    parameter_name='inventory'
    def lookups(self, request,model_admin):
        return[
            ('<10','Low')
        ]
    def queryset(self, request,queryset): 
        if(self.value()=='<10'):
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields=['title']
    # inlines=[TagInline]
    autocomplete_fields=['collection']
    prepopulated_fields={
        'slug':['title']
    }
    # fields=['title','slug']
    actions=['clear_inventory']
    list_display=['title','unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_filter=['collection','last_update',InventoryFilter]
    list_per_page=11
    list_select_related=['collection']
    @admin.action(description="clear inventory")
    def clear_inventory(self,request,queryset):
        updated_count=queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.'
        )
    def collection_title(self,product):
        return product.collection.title
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if(product.inventory<10):
            return 'Low'
        return 'OK'
class OrderItemInline(admin.StackedInline):
    model=models.OrderItem
    autocomplete_fields=['product']
    min_num=1
    max_num =10
    extra=0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields=['customer']
    inlines=[OrderItemInline]    
    list_display=['id','placed_at','customer']
    
    
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership','orders']
    list_editable=['membership']
    ordering=['first_name','last_name']
    list_per_page: 10
    search_fields=['first_name__istartswith','last_name__istartswith']
    # list_select_related=['customer']
     # result=Product.objects.aggregate(count=Count('id'),min_price=Min('unit_price'))
    # def orders(self,order):
    #     return order.orders
    def orders(self,customer):
        return customer.orders
    def get_queryset(self, request): 
        #  return super().get_queryset(request).annotate(orders=Count('order'))
         return super().get_queryset(request).annotate(orders=F('order'))
        # Func(F('first_name'),Value(' '),F('last_name'),function='CONCAT'
    # def order_status(self,obj):
    #     qs=Order.objects.filter(customer=obj.id)
    #     # qs=Order.objects.select_related("customer__customer").filter(customer=obj.id)
        
    #     # orderitems = customer.order.all()
       
    #     return list(qs)
    # def Num_of_orders(self,obj):
    #     result=OrderItem.objects.aggregate(count=Count('quantity'))

    #     return result



# admin.site.register(models.Collection)
admin.site.register(models.Customer,CustomerAdmin)
# admin.site.register(models.Product,ProductAdmin)



@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display=['title','products_count']
    search_fields=['title']
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        # reverse('admin:app_model_page')
        url=(reverse('admin:store_product_changelist') 
        +'?'
        + urlencode({'collection_id':str(collection.id)
        }))
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
         
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))
# Register your models here.

