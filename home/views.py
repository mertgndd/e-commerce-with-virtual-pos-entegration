from django.shortcuts import render,HttpResponse

from order.models import ShopCart
from order.views import *
from tshirt.views import Item
# Create your views here.

def home_view(request):
	current_user = request.user
	request.session['cart_items'] = ShopCart.objects.filter(user_id = current_user.id).count()
	foryou_slider = Item.objects.all().order_by('?')[:8]
	tshirt_slider = Item.objects.filter(category='T-Shirt').order_by('-id')[:8]
	lastitem_slider = Item.objects.all().order_by('-id')[:8]
	sweatshirt_slider = Item.objects.filter(category='Sweatshirt').order_by('-id')[:8]

	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity



	context = {
		'foryou_slider':foryou_slider,
		'tshirt_slider':tshirt_slider,
		'lastitem_slider':lastitem_slider,
		'sweatshirt_slider':sweatshirt_slider,
		'schopcart' : schopcart,
		'total' : total,
	}
	return render(request, 'home/home.html', context)
