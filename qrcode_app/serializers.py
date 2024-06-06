from rest_framework import serializers
from .models import QRCodeTemplate


class QRCodeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCodeTemplate
        fields = '__all__'