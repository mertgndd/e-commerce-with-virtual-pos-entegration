from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Costumer


class LoginForm(forms.Form):
	username = forms.CharField(max_length= 100, label = 'Kullanıcı Adı')
	password = forms.CharField(max_length= 100, label = 'Parola', widget = forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError('Kullanıcı Adı ya da Şifre Hatalı!')
		return super(LoginForm, self).clean()

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username' , 'first_name' , 'last_name', 'password1', 'password2')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password2 != password2:
			raise forms.ValidationError('Girdiğiniz Şifreler Doğrulanamadı. Kontrol Ediniz!')
		return password2




class CostumerForm(forms.ModelForm):

	class Meta:
		model = Costumer
		fields = [
			'phone_number',
			'gender',
			'Adres',
			'email',
		]
		widgets = {
          'Adres': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data.get('email')).exists():
			raise forms.ValidationError('Bu Email Adresi Zaten Sistemde Mevcut!')
		return self.cleaned_data['email']
