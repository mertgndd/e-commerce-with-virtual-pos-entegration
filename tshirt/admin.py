from django.contrib import admin
from .models import Item
# Register your models here.

class ItemAdmin(admin.ModelAdmin):

	list_display = ['id','image','title','publishing_date','urun_adedi','category' ,'slug']
	list_display_links = ['id','title','category','publishing_date','urun_adedi']
	list_filter = ['publishing_date']
	search_fields = ['id', 'title' , 'category']
	#list_editable = ['title']

	class Meta:
		model = Item

admin.site.register(Item, ItemAdmin)
