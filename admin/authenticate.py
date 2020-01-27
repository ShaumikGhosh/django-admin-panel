from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomAuthenticate(ModelBackend):

    def authenticate(self, request, user=None, password=None):
        User = get_user_model()

        try:
            try:
                user = User.objects.get(username=user)
            except:
                user = User.objects.get(email=user)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None