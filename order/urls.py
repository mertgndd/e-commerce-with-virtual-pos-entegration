from django.conf.urls import url
from django.urls import path

from . import views
from .views import *

urlpatterns = [
    # path('shopcart', views.shop_cart_list, name='shopcart'),
    path('addtocart/<int:id>', views.shop_cart_add, name='addtocart'),
    path('deletefromcart/<int:id>', views.shop_cart_delete, name='deletefromcart'),
    path('orderproduct/', views.orderitem, name='siparisver'),
    path('siparis_kaydet/', views.order_list, name='siparis_kaydet'),
    url(r'^siparisler/$', order_list, name='siparisler'),
    url(r'^siparislerim/$', order_list_user, name='siparislerim'),

    path('payment/', payment, name='payment'),
    path('result/', result, name='result'),
    path('success/', success, name='success'),
    path('failure/', fail, name='failure'),

]