from django.shortcuts import render,get_object_or_404
from . import models
import qrcode
import base64
from io import BytesIO
from hd import settings
# Create your views here.
def certificates(request):
    return render(request, 'certificate/certificate.html')

def generate_qr_code_base64(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return img_base64

def certificate(request,uid):
    cert = get_object_or_404(models.Certificate, uid=uid)
    context = {
        'cert': cert,
        'qr_code_base64': generate_qr_code_base64(f'{settings.DOMAIN_NAME}certificate/{cert.uid}/'),
    }
    return render(request, 'certificate/certificate.html',context)