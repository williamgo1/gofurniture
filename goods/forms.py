from django import forms


class GoodsSearchForm(forms.Form):
    search = forms.CharField(max_length=255, required=False, 
                            widget=forms.TextInput(attrs={"class": "form-control", "type": "search", 
                                                          "placeholder": "Название, Артикул", "aria-label": "Поиск"}))


class GoodsFilterForm(forms.Form):
    SORT_CHOICES = [
        ('new', 'Новинки'),
        ('price_asc', 'Сначала дешевые'),
        ('price_desc', 'Сначала дорогие'),
        ("discount", "с наибольшей скидкой")
    ]
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Сортировка', widget=forms.Select({"class": "form-select w-75 mb-3"}))
    min_price = forms.DecimalField(required=False, label='Цена от', widget=forms.NumberInput({"class": "d-inline form-control price-input-w me-2", "placeholder": "От", "type": "search"}))
    max_price = forms.DecimalField(required=False, label='Цена до', widget=forms.NumberInput({"class": "d-inline form-control price-input-w mb-3", "placeholder": "До", "type": "search"}))
    color = forms.CharField(required=False, label='Цвет', widget=forms.TextInput({"class": "form-control w-75 mb-3", "type": "search"}))
    material = forms.CharField(required=False, label='Материал', widget=forms.TextInput({"class": "form-control w-75 mb-3", "type": "search"}))