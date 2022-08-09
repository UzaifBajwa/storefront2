from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_details),
    path('products/', views.show_products),
    path('customer/', views.show_customers),
    path('order/', views.show_orders)
]
