from django.urls import path
from . import views


app_name = 'goods'

urlpatterns = [
    path('', views.GoodsListView.as_view(), name='goods_list'),
    path('category/<slug:category_slug>/', views.GoodsListView.as_view(), name='category_goods_list'),
    path('<slug:slug>/', views.GoodsDetailView.as_view(), name='goods_detail'),
]