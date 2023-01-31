from django.urls import path,include
from . import views

from rest_framework_nested import routers
from pprint import pprint


router=routers.DefaultRouter()    # Parent
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)

products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')
# urlpatterns=router.urls
# URL configuration
urlpatterns= [
        path('',include(router.urls)),
        path('',include(products_router.urls))

#     # path('products/',views.ProductList.as_view()),
#     # path('products/<int:id>/',views.ProductDetail.as_view()),
#     # path('collections',views.CollectionList.as_view()),
#     # path('collections/<int:pk>/',views.CollectionDetail.as_view(),name='detail')
 ]