from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect as Redirect


class UserViewMixin:
    """
    Simple Mixin to shorten code.
    redirect authenticated - if True - redirects authenticated users to the main page.
    """
    form_class = None
    template_name = None
    redirect_authenticated = False
       
    def get(self, request: HttpRequest):
        if self.redirect_authenticated and request.user.is_authenticated:
            return Redirect('/')
        context = {'form': self.form_class}
        return render(request, self.template_name, context)
