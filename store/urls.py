from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]
