"""This module contains the specification of the view used
to create a new menu."""
import json

from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView

from menus.models.menu import Menu

class CreateMenuView(TemplateView):
    """This view renders the required template
    for creating a new menu. Also this view allows
    the creation of a menu"""
    template_name = 'create_menu.html'

    def get(self, request, *args, **kwargs):
        if request.user and not request.user.is_superuser:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user and not request.user.is_superuser:
            return HttpResponseForbidden()
        if not request.user:
            return HttpResponseForbidden()
        data = json.loads(request.body)
        menu = Menu.objects.create_menu(data)
        return HttpResponseRedirect('/menus/')
