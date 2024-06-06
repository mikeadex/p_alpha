from django.http import JsonResponse

class CheckSubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                # Bypass the subscription check for superusers
                return self.get_response(request)
            if not hasattr(request.user, 'profile'):
                return JsonResponse({'error': 'Profile not found'}, status=404)
            if not request.user.profile.is_subscribed:
                return JsonResponse({'error': 'Subscription required'}, status=403)
        return self.get_response(request)
