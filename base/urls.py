from django.urls import path
from . import  views
from account.views import login_page,register,logout_page

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_page, name='logout'),
]