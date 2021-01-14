from django.contrib import admin
from .models import *
# Register your models here.

class ShopCartAdmin(admin.ModelAdmin):
	list_display = ['user', 'item' , 'fiyat', 'quantity' ,'amount' ]
	list_filter = ['user']


class OrderItemline(admin.TabularInline):
	model = OrderItem
	readonly_fields = ('user' , 'item' , 'fiyat', 'quantity')
	can_delete = False
	extra = 0

class OrderItemAdmin(admin.ModelAdmin):
	list_display = ['user', 'item', 'fiyat' , 'quantity']
	list_filter = ['user']
	list_display_links = ['user', 'item' , 'fiyat', 'quantity']
	search_fields = ['user', 'status']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'phone' , 'city', 'total', 'status', 'code','odeme']
	list_display_links = ['first_name', 'last_name', 'phone' , 'city', 'total', 'status', 'code','odeme']
	list_filter = ['status']
	readonly_fields = ('user', 'address' , 'city', 'phone' ,'first_name' , 'ip' , 'last_name', 'phone' , 'city' , 'total', 'sozlesme', 'odeme')
	can_delete = False
	inlines = [OrderItemline]
	search_fields = ['user__username', 'status', 'ip', 'phone' , 'first_name' , 'last_name' , 'code']


admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
