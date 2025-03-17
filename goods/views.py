from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q

from users.models import Cart, Favorite
from .models import Goods, Category
from .forms import GoodsSearchForm, GoodsFilterForm

from utils.queryset_utils import get_annotated_queryset, get_favorites


russian_names = {
    "color": "Цвет",
    "width": "Ширина, см",
    "height": "Высота, cм",
    "depth": "Глубина, см",
    "weight": "Вес, кг",
    "materials": "Материалы",
    "country": "Страна",
    "availability": "Наличие",
    "assembly required": "Требует сборки"
}


class GoodsListView(ListView):
    model = Goods
    extra_context = {'title': 'gofurniture'}
    template_name = 'goods/index.html'
    context_object_name = 'goods_list'
    paginate_by = 18

    def get_template_names(self, *args, **kwargs): 
        if self.request.htmx: 
            return "includes/goods_list.html" 
        else: 
            return self.template_name

    def get_queryset(self):
        goods_filter = GoodsFilterForm(self.request.GET)
        goods_search = GoodsSearchForm(self.request.GET)

        # поиск по названию/артикулу
        if goods_search.is_valid():
            query = goods_search.cleaned_data['search']
            if query:
                goods = Goods.objects.filter(Q(name__icontains=query) | Q(article__icontains=query))
                goods = get_annotated_queryset(goods)
                return goods

        goods = Goods.objects.all()
        # добавляем цены и скидки к товарам
        goods = get_annotated_queryset(goods)

        # Получаем слаг категории из URL
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            # Фильтруем товары по категории
            category = get_object_or_404(Category, slug=category_slug)
            return goods.filter(categories=category)
 
        # фильтрация
        if goods_filter.is_valid():
            sort = goods_filter.cleaned_data.get('sort')
            min_price = goods_filter.cleaned_data.get('min_price')
            max_price = goods_filter.cleaned_data.get('max_price')
            color = goods_filter.cleaned_data.get('color')
            material = goods_filter.cleaned_data.get('material')

            if min_price:
                goods = goods.filter(current_price__gte=min_price)
            if max_price:
                goods = goods.filter(current_price__lte=max_price)
            if color:
                goods = goods.filter(characteristic__color__icontains=color)
            if material:
                goods = goods.filter(characteristic__materials__icontains=material)

            if sort == 'price_asc':
                goods = goods.order_by('current_price')
            elif sort == 'price_desc':
                goods = goods.order_by('-current_price')
            elif sort == 'discount':
                goods = goods.order_by('-discount')
        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_favorites'] = get_favorites(self.request.user)
        context["is_card"] = True
        context['search_form'] = GoodsSearchForm(self.request.GET)
        context['filter_form'] = GoodsFilterForm(self.request.GET)
        context["russian_names"] = russian_names
        # для бесконечной прокрутки htmx
        context["load_url"] = reverse("goods:goods_list")
        return context


class GoodsDetailView(DetailView):
    model = Goods
    template_name = 'goods/goods_detail.html'
    context_object_name = 'goods'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goods = context['goods']
        
        # Получение цен
        prices = goods.prices.order_by('-time_update')
        current_price, old_price = prices.first(), prices.last()

        if self.request.user.is_authenticated:
            # Получаем количество товара в корзине для текущего пользователя
            cart_item = Cart.objects.filter(user=self.request.user, goods=goods).first()
            context['cart_quantity'] = cart_item.quantity if cart_item else 0
        else:
            context['cart_quantity'] = 0

        context['user_favorites'] = get_favorites(self.request.user)
        context['current_price'] = current_price.price
        context['percent'] = current_price.percent
        context['old_price'] = old_price.price
        context['title'] = goods.name
        context["russian_names"] = russian_names
        return context
