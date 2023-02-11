from rest_framework import serializers

from loyalty_management.models import Card, Order, Product


class CardInfoSerializer(serializers.ModelSerializer):
    """Минимальная информация о карте"""
    class Meta:
        model = Card
        fields = ('serial_number', 'number', 'date1', 'date2', 'status')


class CardFullInfoSerializer(serializers.ModelSerializer):
    """Полная информация о карте"""
    class Meta:
        model = Card
        exclude = ('id', )


class OrderInfoSerializer(serializers.ModelSerializer):
    """Информация о заказе"""
    class Meta:
        model = Order
        exclude = ('card', 'id')


class ProductInfoSerializer(serializers.ModelSerializer):
    """Информация о товаре"""
    class Meta:
        model = Product
        exclude = ('order', 'id')
