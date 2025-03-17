from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


app_name = 'users'

urlpatterns = [
    path('registration/', views.UserCreateView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('profile/', views.UserProfileView.as_view(), name='profile'),

    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html', 
        extra_context={'title': 'Пароль успешно изменен!'}), name='password_change_done'),

    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html', 
        email_template_name='users/password_reset_email.html',
        extra_context={'title': 'Сброс пароля',
                       "submit_button": "Сбросить пароль"}, 
        success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html',
        extra_context={'title': 'Сброс пароля'}), 
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html"), name='password_reset_complete'),

    path('<int:goods_id>/toggle_favorite/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite_list'),

    path('cart/add/<int:goods_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:goods_id>/', views.UpdateCartView.as_view(), name='update_cart'),
    path('cart/delete/<int:pk>/', views.delete_from_cart, name='cart_delete'),
    path('cart/', views.CartListView.as_view(), name='cart_list'),

    path('orders/create_order/', views.CreateOrderView.as_view(), name='create_order'),
    path('orders/order_success/', views.order_success, name='order_success'),
    path('orders/order_list/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]