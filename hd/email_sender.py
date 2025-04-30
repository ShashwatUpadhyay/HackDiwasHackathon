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
    