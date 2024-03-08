from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Profile

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                try:
                    profile = Profile.objects.get(user=user)
                    if profile.company is not None and user.email.endswith('@' + profile.company.domain): 
                        return user
                except:
                    return None
                
        return None