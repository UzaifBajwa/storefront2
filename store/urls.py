from cgitb import lookup
from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewVetSet,
                         basename='product-reviews')

urlpatterns = router.urls + products_router.urls


# [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetails.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view()),
#     # path('collections/', views.collection_list),
# path('products/', views.show_products),
# path('customer/', views.show_customers),
# path('order/', views.show_orders)
# ]
