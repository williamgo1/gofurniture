from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.db.models import Q

from users.models import Cart
from .models import Goods, Category
from .forms import GoodsSearchForm, GoodsFilterForm

from utils.queryset_utils import get_favorites, get_cart_quantity, get_filtered_queryset, get_annotated_queryset
from utils.mixins import HTMXTemplateMixin


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


class GoodsListView(HTMXTemplateMixin, ListView):
    model = Goods
    extra_context = {'title': 'gofurniture'}
    template_name = 'goods/index.html'
    context_object_name = 'goods_list'
    paginate_by = 18

    def get_queryset(self):
        goods_filter = GoodsFilterForm(self.request.GET)
        goods_search = GoodsSearchForm(self.request.GET)

        goods = Goods.objects.all()
        goods = get_annotated_queryset(goods)

        # поиск по названию/артикулу
        if goods_search.is_valid():
            query = goods_search.cleaned_data['search']
            if query:
                goods = goods.filter(Q(name__icontains=query) | Q(article__icontains=query))
                return goods
 
        goods = get_filtered_queryset(goods, goods_filter)
        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(parent__isnull=True)  # Только главные категории
        context['user_favorites'] = get_favorites(self.request.user)
        context["is_card"] = True
        context['search_form'] = GoodsSearchForm(self.request.GET)
        context['filter_form'] = GoodsFilterForm(self.request.GET)
        context["russian_names"] = russian_names
        # для бесконечной прокрутки htmx
        context["load_url"] = self.request.path
        return context


class CategoryListView(HTMXTemplateMixin, ListView):
    model = Goods
    template_name = 'goods/category_detail.html'
    context_object_name = 'goods_list'
    paginate_by = 18

    def get_category(self):
        """
        Вспомогательный метод для получения категории.
        """
        category_slug = self.kwargs.get('category_slug')
        subcategory_slug = self.kwargs.get('subcategory_slug', None)

        if subcategory_slug:
            # Если есть подкатегория, получаем её
            return get_object_or_404(
                Category,
                slug=subcategory_slug,
                parent__slug=category_slug
            )
        else:
            # Иначе получаем главную категорию
            return get_object_or_404(Category, slug=category_slug)

    def get_queryset(self):
        goods_filter = GoodsFilterForm(self.request.GET)

        # Получаем товары для категории
        goods = Goods.objects.filter(categories=self.get_category())
        goods = get_annotated_queryset(goods)
        goods = get_filtered_queryset(goods, goods_filter)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.get_category()

        # Добавляем категорию и подкатегории в контекст
        context['category'] = category
        context['subcategories'] = category.children.all()

        context['user_favorites'] = get_favorites(self.request.user)
        context["is_card"] = True
        context['filter_form'] = GoodsFilterForm(self.request.GET)
        context["russian_names"] = russian_names
        context["load_url"] = self.request.path

        # URL для загрузки следующей страницы (для HTMX)
        context['load_url'] = self.request.path

        return context


class GoodsDetailView(DetailView):
    model = Goods
    template_name = 'goods/goods_detail.html'
    context_object_name = 'goods'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goods = context['goods']

        context['cart_quantity'] = get_cart_quantity(self.request.user, goods)
        context['user_favorites'] = get_favorites(self.request.user)
        context['title'] = goods.name
        context["russian_names"] = russian_names

        return context
