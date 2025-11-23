from django.utils.functional import SimpleLazyObject
from customers.models import User

def get_user(request):
    if not hasattr(request, '_cached_user'):
        user_pk = request.session.get('user_pk')
        if user_pk:
            try:
                request._cached_user = User.objects.get(username=user_pk)
            except User.DoesNotExist:
                request._cached_user = None
        else:
            request._cached_user = None
    return request._cached_user

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: get_user(request))
        response = self.get_response(request)
        return response
