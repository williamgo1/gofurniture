from users.models import Cart, Favorite
from goods.models import Price
from django.db.models import OuterRef, Subquery, IntegerField


def get_favorites(user):
    if user.is_authenticated:
        return Favorite.objects.filter(user=user).values_list('goods_id', flat=True)
    else:
        return []


def get_cart_quantity(user, queryset):
    if user.is_authenticated:
            # Получаем количество товара в корзине для текущего пользователя
            cart_item = Cart.objects.filter(user=user, goods=queryset).first()
            return cart_item.quantity if cart_item else 0
    else:
        return 0

def get_annotated_queryset(queryset):
    # Подзапрос для получения текущей цены и скидки
        current_price_subquery = Price.objects.filter(
            goods=OuterRef('pk')
        ).order_by('-time_update').values('price', 'percent')[:1]

        # Подзапрос для старой цены
        old_price_subquery = Price.objects.filter(
            goods=OuterRef('pk')
        ).order_by('time_update').values('price')[:1]

        # Аннотация для цены и скидки
        return queryset.annotate(
            old_price=Subquery(old_price_subquery, output_field=IntegerField()),
            current_price=Subquery(current_price_subquery.values('price'), output_field=IntegerField()),
            current_discount=Subquery(current_price_subquery.values('percent'), output_field=IntegerField()),
        )


def get_filtered_queryset(queryset, filter_form):
    '''Фильтрация товаров'''

    if filter_form.is_valid():
        sort = filter_form.cleaned_data.get('sort')
        min_price = filter_form.cleaned_data.get('min_price')
        max_price = filter_form.cleaned_data.get('max_price')
        color = filter_form.cleaned_data.get('color')
        material = filter_form.cleaned_data.get('material')

        if min_price:
            queryset = queryset.filter(current_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(current_price__lte=max_price)
        if color:
            queryset = queryset.filter(characteristic__color__icontains=color)
        if material:
            queryset = queryset.filter(characteristic__materials__icontains=material)

        if sort == 'price_asc':
            queryset = queryset.order_by('current_price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-current_price')
        elif sort == 'discount':
            queryset = queryset.order_by('-current_discount')
    return queryset