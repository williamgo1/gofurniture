from django.contrib import admin
from .models import Category, Goods, Price


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','article', 'quantity', 'time_update', 'get_categories']
    list_display_links = ['name']
    fields = ['name', 'slug', 'article', 'characteristic', 'description', 'quantity', 'photo', 'categories']
    readonly_fields = ['slug', 'article', 'characteristic', 'description', 'photo']
    ordering = ['-time_update']
    list_filter = ["categories"]
    search_fields = ['name', 'slug', 'article']
    search_help_text = 'Поиск по названию'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('categories')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_display_links = ['name']
    readonly_fields = ['slug']


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['goods', 'price', 'percent']
    list_display_links = ['goods']
    readonly_fields = ['goods']

