from .models import Profile

from django.contrib.auth.models import AnonymousUser


class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            print(type(request.user))
            print(request.user)
            profile = Profile.objects.get(user__id=request.user.id)
            request.profile = profile

        response = self.get_response(request)

        return response
    