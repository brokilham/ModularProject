from django.urls import path
from App_Pulsa.views import penjualan,penjualan_webview,jenis_pulsa,harga,jenis_pulsa_webview, harga_webview

#from . import views

urlpatterns = [
    path('jenis_pulsa', jenis_pulsa.as_view()),
    path('jenis_pulsa_webview', jenis_pulsa_webview.as_view()),
    path('harga', harga.as_view()),
    path('harga_webview', harga_webview.as_view()),
    path('penjualan', penjualan.as_view()),
    path('penjualan_webview', penjualan_webview.as_view()),
   
]

