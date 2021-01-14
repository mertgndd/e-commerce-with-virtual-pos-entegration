from django.shortcuts import render,HttpResponse,get_object_or_404,HttpResponseRedirect,redirect,Http404
from .models import Item
from order.models import ShopCart
from .forms import ItemForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#################################### T-SHİRT ##########################################
def tshirt_index(request):
	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity

	##############################################################

	tshirt_list = Item.objects.filter(category = 'T-Shirt')
	paginator = Paginator(tshirt_list,15)

	page = request.GET.get('sayfa')
	try:
		tshirts = paginator.page(page)
	except PageNotAnInteger:
		tshirts = paginator.page(1)
	except EmptyPage:
		tshirts = paginator.page(paginator.num_pages)

	return render(request, 'items/tshirt/index.html', {'tshirts':tshirts,'schopcart':schopcart,'total':total})


def tshirt_detail(request, slug):
	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity
	########################################################
	tshirt = get_object_or_404(Item, slug=slug)
	context = {
		'tshirt':tshirt,
		'schopcart': schopcart,
		'total' : total,

	}
	return render(request, 'items/tshirt/detail.html', context)

#################################### Eşofman #############################################

def esofman_index(request):
	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity

	##############################################################

	esofman_list = Item.objects.filter(category = 'Esofman')
	paginator = Paginator(esofman_list,15)

	page = request.GET.get('sayfa')
	try:
		esofmans = paginator.page(page)
	except PageNotAnInteger:
		esofmans = paginator.page(1)
	except EmptyPage:
		esofmans = paginator.page(paginator.num_pages)

	return render(request, 'items/esofman/index.html', {'esofmans':esofmans,'schopcart':schopcart,'total':total})


def esofman_detail(request, slug):
	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity
	########################################################
	esofman = get_object_or_404(Item, slug=slug)
	context = {
		'esofman':esofman,
		'schopcart': schopcart,
		'total' : total,

	}
	return render(request, 'items/esofman/detail.html', context)

#################################### SWEATSHİRT ##########################################

def sweatshirt_index(request):
	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity
	######################################################################3
	sweatshirt_list = Item.objects.filter(category = 'Sweatshirt')
	paginator = Paginator(sweatshirt_list,15)

	page = request.GET.get('sayfa')
	try:
		sweatshirts = paginator.page(page)
	except PageNotAnInteger:
		sweatshirts = paginator.page(1)
	except EmptyPage:
		sweatshirts = paginator.page(paginator.num_pages)


	return render(request, 'items/sweatshirt/index.html', {'sweatshirts':sweatshirts, 'schopcart':schopcart, 'total':total})


def sweatshirt_detail(request, slug):
	sweatshirt = get_object_or_404(Item, slug=slug)
	context = {
		'sweatshirt':sweatshirt,
	}
	return render(request, 'items/sweatshirt/detail.html', context)

#################################### KAPİŞONLU ##########################################
def kapisonlu_index(request):
	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity

	#####################################################################################
	kapisonlu_list = Item.objects.filter(category='Kapisonlu')
	paginator = Paginator(kapisonlu_list,15)

	page = request.GET.get('sayfa')
	try:
		kapisonlu = paginator.page(page)
	except PageNotAnInteger:
		kapisonlu = paginator.page(1)
	except EmptyPage:
		kapisonlu = paginator.page(paginator.num_pages)

	return render(request, 'items/kapisonlu/index.html' , {'kapisonlu': kapisonlu,'schopcart':schopcart,'total':total})

def kapisonlu_detail(request,slug):
	kapisonlu = get_object_or_404(Item,slug=slug)
	context = {
		'kapisonlu':kapisonlu,
	}
	return render(request, 'items/kapisonlu/detail.html', context)


#################################### AYAKKABI ##########################################

def aksesuar_index(request):
	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity

	#######################################################################
	aksesuar_list = Item.objects.filter(category = 'Aksesuar')
	paginator = Paginator(aksesuar_list,15)

	page = request.GET.get('sayfa')
	try:
		aksesuar = paginator.page(page)
	except PageNotAnInteger:
		aksesuar = paginator.page(1)
	except EmptyPage:
		aksesuar = paginator.page(paginator.num_pages)

	return render(request, 'items/aksesuar/index.html' , {'aksesuar':aksesuar,'schopcart':schopcart,'total':total})

def aksesuar_detail(request,slug):
	aksesuar = get_object_or_404(Item,slug=slug)
	context = {
		'aksesuar':aksesuar,
	}
	return render(request, 'items/aksesuar/detail.html' , context)

#################################### Oluşturma Ve Güncelleme İşlemleri ##########################################

def items_create(request):
	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity
	###############################################################################################
	for g in request.user.groups.all():
		if g.name == 'yönetim':
			form = ItemForm(request.POST or None , request.FILES or None)
			if form.is_valid():
				item = form.save()
				messages.success(request, 'Ürün İlanı Başarıyla Verildi.', extra_tags='mesaj-basarili')
				return HttpResponseRedirect(item.get_absolute_url())

			return render(request, 'items/form.html', {'form':form,'schopcart':schopcart,'total':total ,'title':'Ürün Ekle'} )
		else:
			raise Http404


def item_update(request, slug):
	current_user = request.user
	schopcart = ShopCart.objects.filter(user__id = current_user.id).order_by('-id')
	total = 0
	for rs in schopcart:
		total += rs.item.fiyat * rs.quantity

	#############################################################################################
	for g in request.user.groups.all():
		if g.name == 'yönetim':
			item = get_object_or_404(Item, slug=slug)
			form = ItemForm(request.POST or None, request.FILES or None ,instance=item)
			if form.is_valid():
				form.save()
				messages.success(request, 'Ürün İlanı Başarıyla Güncellendi')
				return HttpResponseRedirect(item.get_absolute_url())

			return render(request,'items/form.html', {'form':form,'schopcart':schopcart,'total':total ,'title':'Ürün Güncelle'})
		else:
			raise Http404

def item_detail(request,slug):
	item = get_object_or_404(Item, slug=slug)
	context = {
		'item':item
	}
	return render(request, 'items/detail.html' , context)


def item_delete(request, slug):
	for g in request.user.groups.all():
		if g.name == 'yönetim':
			item = get_object_or_404(Item, slug=slug)
			item.delete()

			return redirect('home')
		else:
			raise Http404