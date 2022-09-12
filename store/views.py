from itertools import product
from os import stat
import re
from turtle import title
from urllib import request
from winreg import QueryInfoKey
from . import views
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Sum, Min, Max, Avg
from django.db.models.functions import Concat
from store.models import Cart, CartItem, OrderItem, Product, Customer, Order, Collection
# rest_framework imports
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, CollectionSerializer
from store import serializers

# Creating API views


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            products_count=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@ api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # serializer.validated_data
        return Response(serializer.data)


@ api_view(['GET', 'PUT', 'DELETE'])
def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted,as the product is placed for order'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({'Info': 'Product has been Successfully deleted.'},
                        status=status.HTTP_204_NO_CONTENT)

        """     try:
                    product = Product.objects.get(pk=id)
                    serializer = ProductSerializer(product)
                    return Response(serializer.data)
                except Product.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        """


# Create your views here.


def show_products(request):

    queryset = Collection.objects.filter(id__gt=11).delete()
    return render(request, 'products.html', {'products': list(queryset)})

    # queryset = Collection.objects.filter(featured_product=1).distinct()

    #  discounted_price = ExpressionWrapper(
    #     F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(
    #     discounted_price=discounted_price)

    # queryset = Collection.objects.annotate(product_count=Sum('product'))
    """ queryset = Product.objects.filter(
        collection_id=5).annotate(total_product=Sum('id')) """

    """ queryset = Product.objects.annotate(total_sales=F(
        'orderitem__unit_price') * F('orderitem__quantity')).order_by('-total_sales')[:5] """


"""     collection = Collection(pk=11)
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1)
    result = collection.save()
    return render(request, 'products.html', {'result': result}) """


# queryset = Product.objects.filter(unit_price__gt=20)
# queryset = Product.objects.filter(inventory__lt=10)
# queryset = Product.objects.filter( Q(inventory__lt=10) | ~Q(inventory__gt=20))
# queryset = Product.objects.filter(inventory=F('collection__id'))
# queryset = Product.objects.order_by('unit_price', '-title')
# queryset =  Product.objects.values('id', 'title', 'collection__title')
# queryset = Product.objects.values_list('id', 'title', 'collection__title')

# queryset = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')
# queryset = Product.objects.only('id', 'title')
# queryset = Product.objects.defer('description')

# product = Product.objects.earliest('unit_price')
# return render(request,  'products.html', {'products': product})

# queryset = Product.objects.prefetch_related( 'promotions').select_related('collection')

# What is the min, max and average price of the products in collection 3?
""" result = Product.objects.filter(collection__id=3).aggregate(
        minimum_Order=Min('unit_price'),
        maximum_Order=Max('unit_price'),
        Average_Order=Avg('unit_price'))
    return render(request, 'products.html', {'result': query}) """


def show_customers(request):
    # queryset = Collection.objects.filter(featured_product__isnull=True)

    # queryset = Customer.objects.filter(email__icontains='.com')
    """ queryset = Customer.objects.annotate(full_name=Func(
        F('first_name'), Value(' '), F('last_name'), function='CONCAT')) """

    # queryset = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
    # queryset = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'), Orders_count=Count('order'))

    """ queryset = Customer.objects.annotate(full_name=Concat(
        'first_name', Value(' '), 'last_name'), Last_orders_id=Max('order__id')) """

    """ queryset = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'),
                                         order_count=Count('order')).filter(order_count__gt=5) """

    queryset = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'),
                                         total_amount=Sum(F('order__orderitem__unit_price') * F('order__orderitem__quantity')))

    return render(request, 'customer.html', {'customers': list(queryset)})


def show_orders(request):
    # queryset = Order.objects.filter(customer__id=1)
    # queryset = OrderItem.objects.filter(product__collection__id=3)
    """ Get the last 5 orders with their customers and item (incl prodcut) """
    """ queryset = Order.objects.select_related('customer').prefetch_related(
        'orderitem_set__product').order_by('-placed_at')[:5]

    return render(request, 'order.html', {'orders': list(queryset)}) """

    # result = OrderItem.objects.filter(product__id=1).aggregate(Units_Sold=Sum('quantity'))
    # How mamy orders has the customer 1 placed
    """ result = Order.objects.filter(
        customer__id=1).aggregate(Orders_placed=Sum('id'))
    return render(request, 'order.html', {'result': result}) """
    queryset = Cart.objects.create()
    queryset.save()

    """ queryset = CartItem.objects.create(
        cart_Cart=cart, CartItem_product_id=1, CartItem_quantity=5) """

    return render(request, 'order.html', {'orders': list(queryset)})
