from django.contrib.auth.decorators import login_required

class LoginRequairMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view =  super(LoginRequairMixin,cls).as_view(**initkwargs)
        return login_required(view)