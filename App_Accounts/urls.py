
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.index, name='login'),
    path('login_process', views.login_process, name='login_process'),
    path('logout_process', views.logout_process, name='logout_process'),
]