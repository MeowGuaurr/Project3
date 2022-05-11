from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('cart', views.cart, name='cart'),
    path('confirm_order', views.confirm_order, name='confirm_order'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('delete_item', views.delete_item, name='delete_item'),
    path('check_order', views.check_order, name='check_order')
]