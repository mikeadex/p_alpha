from rest_framework import viewsets, permissions
from .models import QRCodeTemplate
from .serializers import QRCodeTemplateSerializer
import qrcode
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import BusinessInfoForm
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .forms import LoginForm, TwoFactorForm


def generate_qr(request):
    data = request.GET.get('data', 'https://parentskills2go.com')
    img = qrcode.make(data)
    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response


class QRCodeTemplateViewSet(viewsets.ModelViewSet):
    queryset = QRCodeTemplate.objects.all()
    serializer_class = QRCodeTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


@login_required
def generate_custom_qr(request):
    template_id = request.GET.get('template_id')
    data = request.GET.get('data', 'https://example.com')
    template = QRCodeTemplate.objects.get(id=template_id, user=request.user)

    # Customize QR code based on template
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=template.color, back_color="white")

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

@login_required
def complete_business_info(request):
    if request.method == 'POST':
        form = BusinessInfoForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BusinessInfoForm(instance=request.user.profile)
    return render(request, 'qrcode_app/complete_business_info.html', {'form': form})


@login_required
def dashboard(request):
    profile = request.user.profile
    templates = QRCodeTemplate.objects.filter(user=request.user)
    form = BusinessInfoForm(instance=profile)
    return render(request, 'qrcode_app/dashboard.html', {
        'profile': profile,
        'templates': templates,
        'form': form,
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['pre_2fa_user_id'] = user.id
                code = get_random_string(length=6, allowed_chars='0123456789')
                request.session['2fa_code'] = code
                send_mail(
                    'Your 2FA Code',
                    f'Your 2FA code is {code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return redirect('two_factor')
    else:
        form = LoginForm()
    return render(request, 'qrcode_app/login.html', {'form': form})

def two_factor_view(request):
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == request.session.get('2fa_code'):
                user_id = request.session.get('pre_2fa_user_id')
                user = User.objects.get(id=user_id)
                login(request, user)
                return redirect('dashboard')
    else:
        form = TwoFactorForm()
    return render(request, 'qrcode_app/two_factor.html', {'form': form})