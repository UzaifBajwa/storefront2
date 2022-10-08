import collections
from dataclasses import Field, field, fields
from decimal import Decimal
from http.client import ImproperConnectionState
from itertools import product
from logging.config import valid_ident
from operator import mod
from pyexpat import model
from statistics import mode
from unittest.util import _MAX_LENGTH
from xml.sax.handler import property_lexical_handler
from rest_framework import serializers

from store.models import Cart, CartItem, Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    products_count = serializers.IntegerField(read_only=True)

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price',
                  'inventory', 'price_with_tax', 'collection']
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with the given id was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self._validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


# class ProductSerializer(serializers.Serializer):
# id = serializers.IntegerField()
# title = serializers.CharField(max_length=255)
# # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
# price = serializers.DecimalField(
#     max_digits=6, decimal_places=2, source='unit_price')
# price_with_tax = serializers.SerializerMethodField(
#     method_name='calculate_tax')
# Serializing relationship by

# Primarykey
# collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())

# sting
# collection = serializers.StringRelatedField()

# Nested Object
# collection = CollectionSerializer()

# hyperlink
# collection = serializers.HyperlinkedRelatedField(
#     queryset=Collection.objects.all(),
#     view_name='collection-detail'
# )
