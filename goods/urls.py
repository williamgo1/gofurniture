from django.urls import path
from . import views


app_name = 'goods'

urlpatterns = [
    path('', views.GoodsListView.as_view(), name='goods_list'),
    path('<slug:slug>/', views.GoodsDetailView.as_view(), name='goods_detail'),

    path('category/<slug:category_slug>/', views.CategoryListView.as_view(), name='category_detail'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/', views.CategoryListView.as_view(), name='subcategory_detail'),
]
