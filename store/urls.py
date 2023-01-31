from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from pprint import pprint


router=DefaultRouter()
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)
pprint(router.urls)

# urlpatterns=router.urls
# URL configuration
urlpatterns= [
        path('',include(router.urls))
#     # path('products/',views.ProductList.as_view()),
#     # path('products/<int:id>/',views.ProductDetail.as_view()),
#     # path('collections',views.CollectionList.as_view()),
#     # path('collections/<int:pk>/',views.CollectionDetail.as_view(),name='detail')
 ]