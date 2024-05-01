from django.urls import path
# Импортируем созданные нами представления
from .views import *

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', ProductsList.as_view(), name='product_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', ProductDetail.as_view(), name='product_detail'),
   path('create/', ProductCreate.as_view(), name='product_create'),
   path('<int:pk>/edit/', ProductUpdate.as_view(), name='product_edit'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('search/', SearchProduct.as_view(), name='search'),

   ]
