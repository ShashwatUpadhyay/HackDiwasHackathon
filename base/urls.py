from django.urls import path
from . import  views
from account.views import login_page,register

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register, name='register'),
]