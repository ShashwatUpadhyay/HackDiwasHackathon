from django.shortcuts import render , get_object_or_404, redirect
from course.models import Course, Enrollment
from account.models import Student
import razorpay
from django.conf import settings
from hd.settings import DOMAIN_NAME
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
@login_required(login_url='login')
def makepayment(request,uid):
    course = get_object_or_404(Course, uid=uid)
    if hasattr(request.user, 'teacher'):
        messages.error(request, 'Teachers cannot enroll in courses.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    elif request.user.is_superuser:
        messages.error(request, 'Superusers cannot enroll in courses.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    currency = 'INR'
    amount = int(course.discount_price*100) # Rs. 200
    print(course.discount_price,amount)
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = f'{DOMAIN_NAME}payment/course/{uid}/paymenthandler/{request.user.student.uid}/'
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['course'] = course

    
    return render(request,'payment.html',context)

@csrf_exempt
def paymenthandler(request,uid,userid):
    course = get_object_or_404(Course, uid=uid)
    student = get_object_or_404(Student, uid=userid)
    # only accept POST request.
    if request.method == "POST":
        try:
          
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = int(course.discount_price*100)  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    Enrollment.objects.create(
                        student=student,
                        course=course,
                    )
                    messages.success(request, 'Payment Successful! You are now enrolled in the course.')
                    return redirect('course', course.slug)
                except Exception as e:

                    # if there is an error while capturing payment.
                    print(e)
                    messages.success(request, 'Payment Failed!')
                    return redirect('home')
            else:

                # if signature verification fails.
                messages.success(request, 'Payment Failed!')
                return redirect('home')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
