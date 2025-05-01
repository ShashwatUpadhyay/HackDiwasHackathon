from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from . import models
from django.contrib import  messages
from django.http import HttpResponseRedirect
from account.models import Teacher
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

# Create your views here.
def courses(request):
    course = models.Course.objects.filter(is_active = True)
    return render(request,'courses.html',{'courses':course})

def category_courses(request, slug):
    cate = get_object_or_404(models.CourseCategory, slug=slug)
    course = models.Course.objects.filter(is_active = True,category=cate)
    teachers = Teacher.objects.all()
    return render(request,'courses.html',{'courses':course,'cate':cate,'teachers':teachers})

def subcategory_courses(request, slug, sub):
    cate = get_object_or_404(models.CourseCategory, slug=slug)
    subcate = get_object_or_404(models.CourseSubCategory, slug=sub)
    course = models.Course.objects.filter(is_active = True,subcategory=subcate)
    return render(request,'courses-cards.html',{'courses':course,'cate':cate,'subcate':subcate})

def course(request, slug):
    cour = get_object_or_404(models.Course, slug=slug)
    recomm = models.Course.objects.filter(category=cour.category).exclude(uid=cour.uid)[:4]
    return render(request,'class-card.html',{'course':cour,'recomms':recomm})    

def upload_video(request,uid):
    course = get_object_or_404(models.Course, uid=uid)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        freeAccess = request.POST.get('freeAccess')
        file = request.FILES.get('file') 
        print(title, description,file,freeAccess)
        lession = models.Lesson.objects.create(course=course,content=file,description=description,title=title)
        if freeAccess:
            lession.is_free = True
        lession.save()
        messages.success(request, "Video has been uploaded!!.")
        return redirect('videoplayer' , uid = course.uid, v_uid = lession.uid)
    context={
        'course':course,
    }
    return render(request , 'dashboard/upload-content.html',context)

def videoplayer(request,uid, v_uid):
    course = get_object_or_404(models.Course, uid=uid)
    videos = models.Lesson.objects.filter(course=course).order_by('created_at')
    video = models.Lesson.objects.get(uid=v_uid)
    context={
        'course':course,
        'videos':videos,
        'video':video,
    }
    return render(request , 'dashboard/player.html',context)


def mark_complete(request, uid):
    profress = models.Progress.objects.create(student = request.user.student, lesson = get_object_or_404(models.Lesson, uid=uid))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def invoice(request, uid):
    invoice = get_object_or_404(models.Enrollment, uid=uid)
    template_path = 'invoice.html'
    context = {'invoice': invoice}
    
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"Invoice_{invoice.uid}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    
    return HttpResponse("Error generating PDF", status=400)

def detection(request):
    return render(request , 'dashboard/pose-detection.html')