from django import forms
from .models import Item



class ItemForm(forms.ModelForm):

	class Meta:
		model = Item
		fields = [
			'image',
			'title',
			'description',
			'urun_adedi',
			'pre_fiyat',
			'fiyat',
			'category',
			'image2',
			'image3',
			'image4',		
		]