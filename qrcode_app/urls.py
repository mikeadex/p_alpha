from rest_framework.routers import DefaultRouter
from .views import QRCodeTemplateViewSet, generate_custom_qr, generate_qr, complete_business_info, dashboard
from django.urls import path, include

router = DefaultRouter()
router.register(r'templates', QRCodeTemplateViewSet)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('qrcode/', generate_qr, name='generate_qr'),
    path('custom_qrcode/', generate_custom_qr, name='generate_custom_qr'),
    path('complete_business_info/', complete_business_info, name='complete_business_info'),
    path('', include(router.urls)),
]
