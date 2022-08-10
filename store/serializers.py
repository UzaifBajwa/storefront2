import collections
from decimal import Decimal
from http.client import ImproperConnectionState
from itertools import product
from unittest.util import _MAX_LENGTH
from xml.sax.handler import property_lexical_handler
from rest_framework import serializers

from store.models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    # Serializing relationship by

    # Primarykey
    # collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())

    # sting
    # collection = serializers.StringRelatedField()

    # Nested Object
    # collection = CollectionSerializer()

    # hyperlink
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
