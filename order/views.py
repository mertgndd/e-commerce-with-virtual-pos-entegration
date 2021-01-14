from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.utils.crypto import get_random_string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
import random

import iyzipay
import json
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderItem, OrderForm2, StatusForm
from tshirt.models import Item


@login_required
def shop_cart_add(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    product = Item.objects.get(pk=id)

    check_item = ShopCart.objects.filter(item__id=id, user_id=current_user.id)
    if check_item:
        control = 1  # Ürün Sepette Varsa
    else:
        control = 0  # Ürün Sepette Yoksa

    if request.method == 'POST':
        form = ShopCartForm(request.POST or None)
        if form.is_valid():
            if control == 1:  # Ürün Sepette Varsa Güncelle
                data = ShopCart.objects.get(item_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.beden = request.POST.get('beden')
                data.save()
                messages.success(request, "Ürün Sepete Eklenerek Sayısı Güncellenmiştir. Sepetinizi Kontrol Ediniz.")

            else:  # Ürün Sepette Yoksa Ekle
                data = ShopCart()
                data.user_id = current_user.id
                data.item_id = id
                data.quantity = form.cleaned_data['quantity']
                data.beden = request.POST.get('beden')
                data.save()
                messages.success(request, "Ürün Başarı İle Sepete Eklenmiştir. Sepetinizi Kontrol Ediniz.")
        else:
            messages.warning(request, "Lütfen Beden Seçiniz.")
        request.session['cart_items'] = ShopCart.objects.filter(user__id=current_user.id).count()
        return HttpResponseRedirect(url)


    else:
        messages.warning(request, "Lütfen Beden Seçiniz.")

    messages.warning(request, "Ürün Sepete Eklemede Bir Hata Oluştu. Lütfen Sepetinizi Kontrol Ediniz. ")
    return HttpResponseRedirect(url)


@login_required
def shopcart(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'schopcart': schopcart,
        'total': total,
    }
    return render(request, 'order/shopcart_items.html', context)


def shopcart_base(request):
    current_user = request.user
    sepetitem = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in sepetitem:
        total += rs.item.fiyat * rs.quantity

    context = {
        'sepetitem': sepetitem,
        'total': total,
    }
    return render(request, 'header.html', context)


@login_required
def shop_cart_delete(request, id):
    current_user = request.user
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Ürün Sepetten Silindi.")
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    return HttpResponseRedirect("/shopcart")


@login_required
def orderitem(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    schopcart = ShopCart.objects.filter(user_id=current_user.id)

    form = OrderForm(request.POST or None)
    form2 = OrderForm2(request.POST or None)

    total = 0
    for rs in shopcart:
        total += rs.item.fiyat * rs.quantity

    if request.method == 'POST':
        if form.is_valid() and form2.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.address = form2.cleaned_data['address']
            data.city = form2.cleaned_data['city']
            data.phone = form2.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = random.randint(100000000, 999999999)
            # ordercode= get_random_string(9).upper() # random cod
            data.code = ordercode
            data.save()

            for rs in shopcart:
                detail = OrderItem()
                detail.order_id = data.id  # Order Id
                detail.item_id = rs.item_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.beden = rs.beden
                detail.fiyat = rs.item.fiyat
                detail.save()

            return redirect(reverse('payment'))
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    context = {'shopcart': shopcart,
               'total': total,
               'form': form,
               'form2': form2,
               'schopcart': schopcart,
               }
    return render(request, 'order/order_form.html', context)


################### Admin için Sipariş Listeleme ########################
@login_required
def order_list(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    order_list = Order.objects.all().order_by('-id')

    context = {
        'order_list': order_list,
        'schopcart': schopcart,
        'total': total
    }
    return render(request, 'order/all_orders.html', context)


################## Kullanıcı için Sipariş Listeleme ###############################
@login_required
def order_list_user(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    order_list = Order.objects.filter(user_id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'order_list': order_list,
        'schopcart': schopcart,
        'total': total
    }

    return render(request, 'order/my_orders.html', context)


############## Ödeme Yapılan Kısım ################

### Buradaki anahtarlar değişecek

api_key = 'değişecek'
secret_key = 'değişecek'
base_url = 'değişecek'

options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}
sozlukToken = list()

@login_required
def payment(request):
    context = dict()

    current_user = request.user
    order = Order.objects.filter(user__id=current_user.id).last()

    buyer = {
        'id': str(order.user.id),
        'name': str(order.first_name),
        'surname': str(order.last_name),
        'gsmNumber': str(order.phone),
        'email': str(order.email),
        'identityNumber': '11111111111',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': str(order.address),
        'ip': str(order.ip),
        'city': str(order.city),
        'country': 'Turkey',
        # 'zipCode': '34732'
    }

    address = {
        'contactName': str(order.first_name + " " + order.last_name),
        'city': str(order.city),
        'country': 'Turkey',
        'address': str(order.address),
        # 'zipCode': '34732'
    }

    basket_items = [
        {
            'id': str(order.id),
            'name': 'ThePALMZ Giyim',
            'category1': 'Kıyafet',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': str(order.total),
        },
    ]

    request = {
        'locale': 'tr',
        'conversationId': str(order.code),
        'price': str(order.total),
        'paidPrice': str(order.total),
        'currency': 'TRY',
        'basketId': str(order.id),
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://thepalmz.com/order/result/",
        "enabledInstallments": ['2', '3'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    # print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    sozlukToken.append(json_content["token"])
    return HttpResponse(json_content["checkoutFormContent"])


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    current_user = request.user
    order = Order.objects.filter(user__id= current_user.id).last()

    url = request.META.get('index')

    request = {
        'locale': 'tr',
        'conversationId': str(order.code),
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    result = checkout_form_result.read().decode('utf-8')
    sonuc = json.loads(result, object_pairs_hook=list)

    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(url)


def success(request):
    context = dict()

    current_user=request.user
    order=Order.objects.filter(user__id=current_user.id).last()
    order.odeme=True
    order.save()

    ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
    request.session['cart_items'] = 0

    ordermail = Order.objects.filter(user__id=current_user.id).last()
    mailitems = OrderItem.objects.filter(order_id=ordermail.id)


    ctx = {
        'ordercode': order.code,
        'total': order.total,
        'item': mailitems,
        'ordermail': ordermail,
        'orderuser_name': order.first_name,
        'orderuser_surname': order.last_name,
    }
    subject = "ThePALMZ.com | Siparişiniz Alındı."
    from_email = settings.EMAIL_HOST_USER
    to_email = [order.email]
    with open(settings.BASE_DIR + "/templates/order/siparis_olusturuldu.txt") as f:
        siparis_message = f.read()
    message = EmailMultiAlternatives(subject=subject, body=siparis_message, from_email=from_email,
                                     to=to_email)
    html_template = get_template("order/siparis_olusturuldu.html").render(ctx)
    message.attach_alternative(html_template, "text/html")
    message.send()

    ########## Sipariş Oluşumuna Dair Sayfa Yöneticisine Mail Gönderme ############
    subject2 = "ThePALMZ.com | Sipariş Alındı."
    from_email2 = settings.EMAIL_HOST_USER
    to_email2 = ['palmzofficial@gmail.com', 'mertgnd36@gmail.com']
    with open(settings.BASE_DIR + "/templates/order/siparis_olusturuldu.txt") as f:
        siparis_message2 = f.read()
    message2 = EmailMultiAlternatives(subject=subject2, body=siparis_message2, from_email=from_email2,
                                      to=to_email2)
    html_template2 = get_template("order/siparis_olusturuldu_yonetici.html").render(ctx)
    message2.attach_alternative(html_template2, "text/html")
    message2.send()

    context = {
        'ordercode': order.code,
        'order': order,
    }

    return render(request, 'payment/ok.html', context)


def fail(request):
    context = dict()
    context['fail'] = 'İşlem Başarısız'

    current_user = request.user
    ordercount = Order.objects.filter(user__id=current_user.id).count()
    order = Order.objects.filter(user__id=current_user.id).reverse()[ordercount - 1]
    order.delete()

    template = 'payment/fail.html'
    return render(request, template, context)