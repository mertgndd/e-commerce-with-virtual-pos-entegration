from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput

from tshirt.models import Item


class ShopCart(models.Model):
    BEDEN_CHOICES = (
        ('', 'Beden Seçiniz.'),
        ('S-M', 'S-M'),
        ('L-XL', 'L-XL'),
        ('Tek Ebat', 'Tek Ebat'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    beden = models.CharField(max_length=10, null=False, blank=False, choices=BEDEN_CHOICES)
    ordered = models.BooleanField(default=False)

    @property
    def amount(self):
        return (self.quantity * self.item.fiyat)

    @property
    def fiyat(self):
        return (self.item.fiyat)


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = {'quantity', 'beden'}
        widgets = {
            'quantity': TextInput(attrs={'class': 'input', 'type': 'number', 'value': '1'}),
        }


class Order(models.Model):
    STATUS = (
        ('Yeni', 'Yeni'),
        ('Kabul Edildi', 'Kabul Edildi'),
        ('Hazırlanıyor', 'Hazırlanıyor'),
        ('Sipariş Kargoya Verildi', 'Sipariş Kargoya Verildi'),
        ('Sipariş Tamamlandı', 'Sipariş Tamamlandı'),
        ('İptal Edildi', 'İptal Edildi'),

    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=9, editable=False, verbose_name='Sipariş Kodu')
    email = models.EmailField(null=False, blank=False, verbose_name='Email')
    first_name = models.CharField(max_length=15, verbose_name='Ad', null=True, blank=False)
    last_name = models.CharField(max_length=20, verbose_name='Soyad', null=True, blank=False)
    phone = models.CharField(blank=False, max_length=11, verbose_name='Telefon Numarası')
    address = models.CharField(blank=False, max_length=150, verbose_name='Adres')
    city = models.CharField(blank=False, max_length=28, verbose_name='Şehir')
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Toplam Tutar')
    status = models.CharField(max_length=12, choices=STATUS, default='Yeni', verbose_name='Sipariş Durumu')
    sozlesme = models.BooleanField("Mesafeli Satış Sözleşmesi & Şartlar Ve Koşulları Okudum ve Onaylıyorum",
                                   default=True)
    ip = models.CharField(blank=True, max_length=28)
    adminnote = models.CharField(blank=True, max_length=100, verbose_name='Yönetici Notu')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    odeme = models.BooleanField(default=0)

    def __str__(self):
        return self.user.first_name

    def get_absolute_url(self):
        return reverse('order:detail', kwargs={'id': self.id})


class StatusForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email']


class OrderForm2(ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone', 'city']


class OrderItem(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    beden = models.CharField(max_length=12, null=False, blank=False)
    fiyat = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item.title


