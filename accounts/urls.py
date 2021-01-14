from django.conf.urls import url
from .views import *

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^SSS/$', sss_view, name='sss'),
    url(r'^hakkimizda/$', hakkimizda_view, name='hakkimizda'),
    url(r'^kargo-süreci/$', kargo_sureci_view, name='kargo-süreci'),
    url(r'^degisim-iade/$', degisim_iade_view, name='degisim-iade'),
    url(r'^sartlar-kosullar/$', sartlar_kosullar_view, name='sartlar-kosullar'),
    url(r'^mesafeli-satis-sozlesmesi/$', mesafeli_satis_sozlesmesi_view, name='mesafeli-satis-sozlesmesi'),
    url(r'^gizlilik/$', gizlilik_view, name='gizlilik'),
    url(r'^iletisim/$', iletisim_view, name='iletisim'),

]