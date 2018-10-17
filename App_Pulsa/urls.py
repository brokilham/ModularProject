from django.urls import path
from App_Pulsa.views import penjualan,jenis_pulsa,harga,jenis_pulsa_weblist

#from . import views

urlpatterns = [
    path('jenis_pulsa', jenis_pulsa.as_view()),
    path('jenis_pulsa_weblist', jenis_pulsa_weblist.as_view()),
    path('harga', harga.as_view()),
    #path('penjualan',  penjualan.as_view()),
   
]

