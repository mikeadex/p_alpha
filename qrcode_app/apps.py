from django.apps import AppConfig

class QrcodeAppConfig(AppConfig):
    name = 'qrcode_app'

    def ready(self):
        import qrcode_app.signals
