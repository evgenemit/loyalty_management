from django.contrib import admin

from .models import Card, Order, Product


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
	list_display = ('serial_number', 'number', 'status', 'discount')
	list_display_links = ('number', )
	list_editable = ('status', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('number', 'order_sum', 'discount_sum')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'discount_price')
