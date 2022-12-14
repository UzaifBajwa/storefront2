from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Sum, Min, Max, Avg
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from store.models import Cart, CartItem, OrderItem, Product, Customer, Order, Collection
# rest_framework imports
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from store.pagination import DefaultPagination
from .models import Product, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer
# from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer
from .filters import ProductFilter


# Creating Generic API views

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Collection.products.objects.filter(colllection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted,as the product is placed for order'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewVetSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')


# function based views


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
