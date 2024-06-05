import qrcode
from django.http import HttpResponse


def generate_qr(request):
    data = request.GET.get('data', 'https://parentskills2go.com')
    img = qrcode.make(data)
    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response
