from django.shortcuts import render, redirect
from .forms import LoginForm, CostumerForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from order.models import ShopCart


# Create your views here.


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form, 'title': 'Giriş Yap'})


########### sık Sorulan Sorular View ###########################


def sss_view(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'schopcart': schopcart,
        'total': total,
    }
    return render(request, 'home/sss.html', context)


################ Hakkımızda Sayfası View #######################

def hakkimizda_view(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'schopcart': schopcart,
        'total': total,
    }
    return render(request, 'home/hakkimizda.html', context)


############  Kargo Süreci View ###########################

def kargo_sureci_view(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'schopcart': schopcart,
        'total': total,
    }
    return render(request, 'home/kargo_sureci.html', context)


############ Değişim ve İade Süreci View ###################

def degisim_iade_view(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'schopcart': schopcart,
        'total': total,
    }
    return render(request, 'home/degisim_iade.html', context)


############# Şartlar Ve Koşullar View #####################

def sartlar_kosullar_view(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'schopcart': schopcart,
        'total': total,
    }
    return render(request, 'home/sartlar_kosullar.html', context)


######### Mesafeli Satış Sözleşmesi View ##################

def mesafeli_satis_sozlesmesi_view(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'schopcart': schopcart,
        'total': total,
    }
    return render(request, 'home/mesafeli_satis_sozlesmesi.html', context)


########## Gizlilik View #################################

def gizlilik_view(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'schopcart': schopcart,
        'total': total,
    }
    return render(request, 'home/gizlilik.html', context)


########### İletişim View #################################

def iletisim_view(request):
    current_user = request.user
    schopcart = ShopCart.objects.filter(user__id=current_user.id).order_by('-id')
    total = 0
    for rs in schopcart:
        total += rs.item.fiyat * rs.quantity

    context = {
        'schopcart': schopcart,
        'total': total,
    }
    return render(request, 'home/iletisim.html', context)


######### Kayıt Olma View #################################

def register_view(request):
    form = UserForm(request.POST or None)
    form2 = CostumerForm(request.POST or None)

    CostumerGroup = Group.objects.get(name='costumer')

    if form.is_valid() and form2.is_valid():
        user = form.save()
        CostumerGroup.user_set.add(user)
        costumer = form2.save(commit=False)
        costumer.user = user
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('home')

    return render(request, 'accounts/register.html', {'form': form, 'form2': form2, 'title': 'Yeni Kullanıcı Oluştur!'})


######### Çıkış Yapma #################################

def logout_view(request):
    logout(request)
    return redirect('accounts:login')