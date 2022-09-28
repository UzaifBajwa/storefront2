from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetails.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.collection_detail),
    # path('collections/', views.collection_list),
    path('products/', views.show_products),
    path('customer/', views.show_customers),
    path('order/', views.show_orders)
]
