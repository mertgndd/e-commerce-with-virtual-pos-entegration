from django.conf.urls import url
from .views import *

app_name = 'item'

urlpatterns = [
    url(r'^create/$', items_create, name='create'),

    url(r'^tshirt/$', tshirt_index, name='tshirt'),
    url(r'^sweatshirt/$', sweatshirt_index, name='sweatshirt'),
    url(r'^aksesuar/$', aksesuar_index, name='aksesuar'),
    url(r'^kapisonlu/$', kapisonlu_index, name='kapisonlu'),
    url(r'^esofman/$', esofman_index, name='esofman'),

    url(r'^(?P<slug>[\w-]+)/$', tshirt_detail, name='tshirt-detail'),
    url(r'^(?P<slug>[\w-]+)/$', sweatshirt_detail, name='sweatshirt-detail'),
    url(r'^(?P<slug>[\w-]+)/$', kapisonlu_detail, name='kapisonlu-detail'),
    url(r'^(?P<slug>[\w-]+)/$', aksesuar_detail, name='aksesuar-detail'),
    url(r'^(?P<slug>[\w-]+)/$', esofman_detail, name='esofman-detail'),

    url(r'^(?P<slug>[\w-]+)/$', item_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', item_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', item_delete, name='delete'),

]