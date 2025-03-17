from django.db.models import OuterRef, Subquery, IntegerField
from users.models import Favorite
from goods.models import Price


def get_annotated_queryset(queryset):
    # Подзапрос для старой цены
    old_price_subquery = Price.objects.filter(
        goods=OuterRef('pk')
    ).order_by('time_update').values('price')[:1]

    # Подзапрос для текущей цены
    current_price_subquery = Price.objects.filter(
        goods=OuterRef('pk')
    ).order_by('-time_update').values('price')[:1]

    # Подзапрос для скидки
    discount_subquery = Price.objects.filter(
        goods=OuterRef('pk')
    ).order_by('-time_update').values('percent')[:1]

    # добавление вычисляемых полей: цены и скидка
    queryset = queryset.annotate(
        old_price=Subquery(old_price_subquery, output_field=IntegerField()),
        current_price=Subquery(current_price_subquery, output_field=IntegerField()),
        discount=Subquery(discount_subquery, output_field=IntegerField())
    )
    return queryset


def get_favorites(user):
    if user.is_authenticated:
        return Favorite.objects.filter(user=user).values_list('goods_id', flat=True)
    else:
        return tuple()
            