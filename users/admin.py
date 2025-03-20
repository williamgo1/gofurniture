from django.contrib import admin
from .models import Favorite, Cart, Order, OrderItem


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'created_at']
    list_display_links = ['user', 'goods']
    readonly_fields = ['user', 'goods']
    list_filter = ["user"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'quantity', 'added_at']
    list_display_links = ['user', 'goods']
    readonly_fields = ['user', 'goods', 'quantity']
    list_filter = ["user"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_total_cost', 'phone', 'created_at', 'status']
    list_display_links = ['__str__']
    list_editable = ['status']
    readonly_fields = ['user', 'get_total_cost', 'phone', 'address', 'created_at']
    list_filter = ["user"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods', 'get_total_cost', 'quantity']
    list_display_links = ['order']
    readonly_fields = ['order', 'goods', 'get_total_cost', 'quantity']
    list_filter = ["order"]
