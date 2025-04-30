from django.urls import path
from . import views
urlpatterns = [
    path('course/<uid>/',views.makepayment,name='makepayment'),
    path('course/<uid>/paymenthandler/<userid>/', views.paymenthandler, name='paymenthandler'),
]