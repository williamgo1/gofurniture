from django.db import models
from django.contrib.auth.models import User
from goods.models import Goods
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.humanize.templatetags.humanize import intcomma


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="Товар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")

    class Meta:
        unique_together = ('user', 'goods')  # чтобы товар нельзя было добавить дважды
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")

    def __str__(self):
        return f"{self.user.username} - {self.goods.name} (x{self.quantity})"
    
    def get_current_total_cost(self):
        """Возвращает общую стоимость товара с учетом актуальной цены."""
        # Получаем последнюю обновленную цену товара
        price = self.goods.get_current_price()
        return price * self.quantity
    
    def get_origin_total_cost(self):
        """Возвращает общую стоимость товара с учетом актуальной цены."""
        # Получаем последнюю обновленную цену товара
        price = self.goods.get_origin_price()
        return price * self.quantity

    class Meta:
        unique_together = ('user', 'goods')
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    


class Order(models.Model):
    # Статусы заказов
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Активный'),
        (STATUS_COMPLETED, 'Завершенный'),
        (STATUS_CANCELLED, 'Отмененный'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = PhoneNumberField(region='RU', verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, 
                              default=STATUS_ACTIVE, verbose_name='Статус заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"
    
    def get_total_cost(self):
        """Возвращает общую стоимость заказа."""
        return sum(item.get_total_cost() for item in self.items.all())
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f"{self.goods.name} ({self.quantity} шт.)"
    
    def get_total_cost(self):
        """Возвращает общую стоимость товара с учетом актуальной цены."""
        # Получаем последнюю обновленную цену товара
        price = self.goods.get_current_price()
        return price * self.quantity

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
