import json
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, logout

from .models import Favorite, Cart, Order, OrderItem
from goods.models import Goods, Price
from .forms import UserCreateForm, UserLoginForm, UserPasswordChangeForm, UserUpdateForm, OrderForm

from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import OuterRef, Subquery, IntegerField, Case, When, Value

from goods.views import russian_names
from utils.queryset_utils import get_annotated_queryset, get_favorites


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Профиль',
                     "submit_button": "Сохранить изменения"
                     }
    
    def get_object(self, queryset=None):
        return self.request.user


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация',
                     "submit_button": "Зарегистироваться"
                     }


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Авторизация',
                     "submit_button": "Войти"
                     }


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('goods:goods_list'))


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Изменение пароля',
                     "submit_button": "Изменить пароль"
                     }


class ToggleFavoriteView(LoginRequiredMixin, View):
    """
    Класс для добавления товара в избранное через AJAX.
    """
    def post(self, request, *args, **kwargs):
        goods_id = kwargs.get('goods_id')  # Получаем ID товара из URL
        goods = get_object_or_404(Goods, id=goods_id)  # Находим товар
        favorite, created = Favorite.objects.get_or_create(user=request.user, goods=goods)  # Добавляем в избранное
        
        if not created:
            # Если запись уже существует, удаляем ее
            favorite.delete()
            return JsonResponse({'success': True, 'action': 'removed'})
        else:
            # Если запись создана, добавляем товар в избранное
            return JsonResponse({'success': True, 'action': 'added'})


class FavoriteListView(LoginRequiredMixin, ListView):
    """
    Класс для отображения списка избранных товаров.
    """
    template_name = 'users/favorite_list.html'
    context_object_name = 'favorite_goods'
    extra_context = {
        "russian_names": russian_names,
        'title': 'Избранное',
    }

    def get_template_names(self, *args, **kwargs): 
        if self.request.htmx: 
            return "includes/goods_list.html" 
        else: 
            return self.template_name

    def get_queryset(self):
        favorite_goods = Goods.objects.filter(favorite__user=self.request.user)
        favorite_goods = get_annotated_queryset(favorite_goods)
        return favorite_goods
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_favorites'] = get_favorites(self.request.user)
        context["is_card"] = True
        context["load_url"] = reverse("users:favorite_list")
        return context


class CartListView(LoginRequiredMixin, ListView):
    """
    Класс для отображения корзины.
    """
    model = Cart
    template_name = 'users/cart_list.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related('goods')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']

        for item in cart_items:
            # Получаем первую цену (самая старая цена)
            old_price = Price.objects.filter(goods=item.goods).order_by('time_update').first()
            item.old_price = old_price.price
            
            # Получаем последнюю цену (самая новая цена)
            current_price = Price.objects.filter(goods=item.goods).order_by('-time_update').first()
            item.current_price = current_price.price
            item.discount = current_price.percent
            
            # Вычисляем старая сумму
            item.total_old_amout = item.old_price * item.quantity

            # Вычисляем текущую сумму
            item.total_current_amout = item.current_price * item.quantity
        
        # Вычисляем общую сумму для всех товаров в корзине
        total_amount = sum(item.total_current_amout for item in cart_items)

        context['user_favorites'] = get_favorites(self.request.user)
        context["is_card"] = False

        context["title"] = "Корзина"
        context["total_amount"] = total_amount
        return context


class AddToCartView(LoginRequiredMixin, View):
    """
    Класс для добавления товара в корзину.
    """
    def post(self, request, *args, **kwargs):
        goods_id = kwargs.get('goods_id')
        goods = get_object_or_404(Goods, id=goods_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, goods=goods)

        if not created:
            # Если товар уже в корзине, увеличиваем количество
            cart_item.quantity += 1
            cart_item.save()
            action = 'updated'
        else:
            action = 'added'

        return JsonResponse({'success': True, 'action': action})


@require_POST
def delete_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    return JsonResponse({'status': 'success'})


class UpdateCartView(LoginRequiredMixin, View):
    """
    Класс для обновления количества товара в корзине.
    """
    def post(self, request, *args, **kwargs):
        goods_id = kwargs.get('goods_id')
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        # quantity = int(request.POST.get('quantity'))  # Получаем количество из запроса

        # Находим товар в корзине пользователя
        cart_item = get_object_or_404(Cart, user=request.user, goods_id=goods_id)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Удаляем товар из корзины, если количество равно 0

        return JsonResponse({'success': True})


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'users/create_order.html'
    success_url = reverse_lazy('users:order_success')
    extra_context = {"title": "Оформление заказа",
                     "submit_button": "Оформить заказ"
                     }

    def form_valid(self, form):
        # Привязываем заказ к текущему пользователю
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Переносим товары из корзины в заказ
        cart_items = Cart.objects.filter(user=self.request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=self.object,  # self.object — это созданный заказ
                goods=item.goods,
                quantity=item.quantity
            )
            item.delete()  # Очищаем корзину
        return response


def order_success(request):
    data = {"title": "Заказ Заказ успешно оформлен!"}
    return render(request, "users/order_success.html", context=data)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'users/order_list.html'
    context_object_name = 'orders'
    extra_context = {"title": "Заказы"}

    def get_queryset(self):
        # Сортировка: сначала активные, затем по дате создания
        return Order.objects.filter(user=self.request.user).annotate(
            status_order=Case(
                When(status='active', then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by('status_order', '-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'users/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
