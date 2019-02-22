from django.contrib.auth.models import User


class SocialAuthBackend:

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(request, usertoken):
        pass

    #def authenticate(request, usernam):
        # lookup in our user db for user that is tied to usertoken from [Discord]
        # if it exists, return the user that matches
        # if it doesnt, create the user entry tied to that social auth provider then return it
