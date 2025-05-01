from django.core.mail import send_mail
from . import settings
from django.core.mail import EmailMultiAlternatives


def verifyUser(email,uid):
    try:
        send_mail(
                    'Verify your account!',
                    'Verify your account',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                    html_message=f"""<p>
                        <h1>Click the button below to verify your account 👇!</h1>
                        <button><a href='{settings.DOMAIN_NAME}user/verify/{uid}/'>OPEN</a></button>
                        
                    </p>"""
                )
    except Exception as e:
        print(e)
    
def course_purchased(instance):
    try:
        send_mail(
    'Welcome to the Course – Your Enrollment is Confirmed!',
    'You are now enrolled in the course!',
    settings.EMAIL_HOST_USER,
    [instance.student.user.email],
    fail_silently=False,
    html_message=f"""
                    <div style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                        <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <h2 style="color: #2c3e50;">🎉 Welcome to Your New Learning Journey!</h2>
                            <p style="font-size: 16px; color: #555;">
                                Hi {instance.student.full_name if instance.student.full_name else ''},
                            </p>
                            <p style="font-size: 16px; color: #555;">
                                You've successfully enrolled in the course. We're thrilled to have you on board and can’t wait to see what you’ll achieve!
                            </p>
                            <p style="font-size: 16px; color: #555;">
                                To get started, you can download your course invoice below:
                            </p>
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{settings.DOMAIN_NAME}courses/enrolled/invoice/{instance.uid}/" 
                                style="background-color: #007BFF; color: white; padding: 12px 20px; border-radius: 5px; text-decoration: none; font-weight: bold;">
                                    📄 Download Invoice
                                </a>
                            </div>
                            <p style="font-size: 14px; color: #999;">If you have any questions, feel free to reach out to our support team.</p>
                            <p style="font-size: 14px; color: #999;">Happy Learning!<br>The Team</p>
                        </div>
                    </div>
                    """
                )

    except Exception as e:
        print(e)
    