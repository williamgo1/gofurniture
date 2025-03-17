import json
from random import randint
import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gofurniture.settings')
# Set up Django
django.setup()

from goods.models import Goods, Category, Price


with open("sst-dizajnerskie.json", encoding="utf-8") as file:
    items = json.load(file)

for item in items:
    item["characteristic"].pop("Название")
    item["characteristic"].pop("Наличие")
    item["characteristic"].pop("Доставка")
    if item["characteristic"].get("Глубина, см"):
        item["characteristic"]["depth"] = item["characteristic"].pop("Глубина, см")
    if item["characteristic"].get("Ширина, см"):
        item["characteristic"]["width"] = item["characteristic"].pop("Ширина, см")
    if item["characteristic"].get("Высота, cм"):
        item["characteristic"]["height"] = item["characteristic"].pop("Высота, cм")
    if item["characteristic"].get("Вес, кг"):
        item["characteristic"]["weight"] = item["characteristic"].pop("Вес, кг")
    if item["characteristic"].get("Вес, кг"):
        item["characteristic"]["weight"] = item["characteristic"].pop("Вес, кг")

    if item["characteristic"].get("Страна"):
        item["characteristic"]["country"] = item["characteristic"].pop("Страна")
    if item["characteristic"].get("Цвет"):
        item["characteristic"]["color"] = item["characteristic"].pop("Цвет")
    if item["characteristic"].get("Материалы"):
        item["characteristic"]["materials"] = item["characteristic"].pop("Материалы")
    if item["characteristic"].get("Требует сборки"):
        item["characteristic"]["assembly required"] = item["characteristic"].pop("Требует сборки")


category1, created = Category.objects.get_or_create(name="Кресла")
category2, created = Category.objects.get_or_create(name="Дизайнерские кресла")

for item in items:
    goods = Goods.objects.filter(article=item["article"]).first()

    if goods:
        print(goods.article)
        # goods.categories.add(category1)
        # goods.categories.add(category2)
    else:
        goods = Goods(name=item["name"], article=item["article"], characteristic=item["characteristic"], quantity=randint(10, 30), photo=f"dizajnerskie-kresla/images/{item['article']}.jpg")
        
        description = item["description"]
        if description:
            goods.description = description
        goods.save()
        goods.categories.add(category1)
        goods.categories.add(category2)
        goods.save()

        if item.get("old_price"):
            price = int(item["old_price"])
            goods_price = Price(price=price, percent=0, goods=goods)
            goods_price.save()
            
            price = int(item["price"])
            percent = item["percent"]
            goods_price = Price(price=price, percent=percent, goods=goods)
            goods_price.save()
        else:
            price = int(item["price"])
            goods_price = Price(price=price, percent=0, goods=goods)
            goods_price.save()
