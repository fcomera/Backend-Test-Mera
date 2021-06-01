"""This module contains the view responsible of showing the landing
page"""
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class Index(TemplateView):
    """This view"is responsible of redirecting the user
    to the correspondant index view. It can be
    the login, the list menu or the selections of
    an employee"""

    def get(self, request, *args, **kwargs):
        """Redirect the user to the correspondant landing page"""
        if request.user and request.user.is_superuser:
            return HttpResponseRedirect('menus/')
        if request.user and not request.user.is_superuser:
            return HttpResponseRedirect('employee/orders/')
        return HttpResponseRedirect('accounts/login/')
