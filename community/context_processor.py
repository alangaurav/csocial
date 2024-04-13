from .models import Profile

def profile_context(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        return {'user_profile' : profile}
    else:
        return {}
