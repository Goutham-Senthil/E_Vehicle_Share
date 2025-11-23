from django.contrib.auth.backends import BaseBackend
from customers.models import User

class UsernameAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_pk):
        try:
            # Get user using `username` as the primary key
            return User.objects.get(username=user_pk)
        except User.DoesNotExist:
            return None
