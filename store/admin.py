
from django.db.models.aggregates import Count
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html,urlencode
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_per_page=11
    list_select_related=['collection']

    def collection_title(self,product):
        return product.collection.title
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if(product.inventory<10):
            return 'Low'
        return 'OK'

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','placed_at','customer']
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    list_editable=['membership']
    ordering=['first_name','last_name']
    # list_select_related: ['Order']
    # def no_of_orders(self,Customer):
    #     return customer.order.quantity


# admin.site.register(models.Collection)
admin.site.register(models.Customer,CustomerAdmin)
# admin.site.register(models.Product,ProductAdmin)



@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display=['title','products_count']
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

