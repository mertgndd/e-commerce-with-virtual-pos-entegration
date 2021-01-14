from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime


class Costumer(models.Model):
	GENDER_CHOİCES = (
			('' , 'Cinsiyet Seçiniz'),
			('Kadın' , 'Kadın'),
			('Erkek' , 'Erkek'),
		)

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	phone_number = models.CharField(max_length=11, null = False, blank = False, unique = True, verbose_name="Telefon Numarası")
	gender = models.CharField(max_length=20, blank=False, null= False, choices = GENDER_CHOİCES, verbose_name="Cinsiyet")
	Adres = models.TextField(null = False, blank=False)
	email = models.EmailField(null = True)


