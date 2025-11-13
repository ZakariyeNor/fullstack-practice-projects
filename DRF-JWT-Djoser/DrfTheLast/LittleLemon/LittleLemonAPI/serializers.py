from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal

import bleach


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(
        method_name= 'calculate_tax'
    )
    category = CategorySerializer()
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
    
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(6.0)
    
    def validate_title(self, value):
        # Clean title field to remove unsafe HTML/script tags
        return bleach.clean(value)