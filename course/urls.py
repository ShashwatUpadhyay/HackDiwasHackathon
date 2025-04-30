from django.urls import path
from . import views
urlpatterns = [
    path('',views.courses,name='courses'),
    path('category/<slug>/',views.category_courses,name='cate_courses'),
    path('category/<slug>/<sub>/',views.subcategory_courses,name='subcate_courses'),
]