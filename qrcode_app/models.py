from django.db import models
from django.contrib.auth.models import User


class QRCodeTemplate(models.Model):
    name = models.CharField(max_length=100)
    design = models.TextField()
    color = models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='banners/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class QRCodeScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ForeignKey(QRCodeTemplate, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.username} scanned {self.qr_code.name} at {self.scanned_at}"


class BusinessCardView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.username} business card viewed at {self.viewed_at}"
