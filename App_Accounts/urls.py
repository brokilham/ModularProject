
from django.urls import path
from . import views

urlpatterns = [
    # ex: /polls/
    path('login', views.index, name='login'),
    path('login_process', views.login_process, name='login_process'),
    path('logout_process', views.logout_process, name='logout_process'),
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    #path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]