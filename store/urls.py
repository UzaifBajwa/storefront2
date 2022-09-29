from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls

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
