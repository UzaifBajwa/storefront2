import collections
from dataclasses import Field, field, fields
from decimal import Decimal
from http.client import ImproperConnectionState
from itertools import product
from pyexpat import model
from statistics import mode
from unittest.util import _MAX_LENGTH
from xml.sax.handler import property_lexical_handler
from rest_framework import serializers

from store.models import Product, Collection, Review


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
