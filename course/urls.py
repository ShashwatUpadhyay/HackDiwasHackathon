from django.urls import path
from . import views
urlpatterns = [
    path('',views.courses,name='courses'),
    path('detection/',views.detection,name='detection'),
    path('<slug>/',views.course,name='course'),
    path('category/<slug>/',views.category_courses,name='cate_courses'),
    path('category/<slug>/<sub>/',views.subcategory_courses,name='subcate_courses'),
    path('<uid>/video/<v_uid>/',views.videoplayer,name='videoplayer'),
    path('<uid>/upload-video/',views.upload_video,name='upload_video'),
    path('mark_complete/<uid>/',views.mark_complete,name='mark_complete'),
    path('enrolled/invoice/<uid>/',views.invoice,name='invoice'),
]