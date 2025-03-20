from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from unidecode import unidecode


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    photo = models.ImageField(max_length=100, null=True, blank=True, verbose_name='Фото категории')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children',
                               verbose_name='Родительская категория'
                               )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Возвращает URL категории с учетом вложенности."""
        if self.parent:
            # Если это подкатегория, используем маршрут для подкатегорий
            return reverse('goods:subcategory_detail', args=[self.parent.slug, self.slug])
        # Если это главная категория, используем маршрут для категорий
        return reverse('goods:category_detail', args=[self.slug])
        # return reverse('goods:category', kwargs={"cat_slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Goods(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    article = models.CharField(max_length=30, unique=True, verbose_name="Артикул")
    description = models.TextField(blank=True, verbose_name="Описание")
    characteristic = models.JSONField(verbose_name="Характеристика")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    photo = models.ImageField(max_length=100, verbose_name='Фото Товара')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    categories = models.ManyToManyField(Category, related_name='goods', verbose_name='Категории')

    def __str__(self):
        return self.name

    def get_current_price(self):
        """Возвращает актуальную цену товара."""
        current_price = self.prices.order_by('-time_update').first()
        if current_price:
            return current_price.price
        return 0

    def get_current_discount(self):
        """Возвращает актуальную цену товара."""
        current_price = self.prices.order_by('-time_update').first()
        if current_price:
            return current_price.percent
        return 0

    def get_origin_price(self):
        """Возвращает начальную цену товара."""
        origin_price = self.prices.order_by('time_update').first()
        if origin_price:
            return origin_price.price
        return 0

    def get_absolute_url(self):
        return reverse('goods:goods_detail', kwargs={"slug": self.slug})
    
    def get_categories(self):
        return ", ".join([category.name for category in self.categories.all()])
    get_categories.short_description = 'Категории'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        counter = 1

        while Goods.objects.filter(slug=self.slug).exists():
            self.slug = f"{self.slug}-{counter}"
            counter += 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-time_update']


class Price(models.Model):
    price = models.PositiveIntegerField(verbose_name="Цена")
    percent = models.PositiveSmallIntegerField(verbose_name="Скидка")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="Товар", related_name="prices")
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return f"{self.price}"

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"
        ordering = ['-time_update']

    # def save(self, *args, **kwargs):
    #     origin_price = Price.objects.filter(self.goods)
    #     self.percent = 
    #     return super().save(*args, **kwargs)
