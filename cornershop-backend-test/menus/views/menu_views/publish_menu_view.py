"""This module contains the specification of the view
that publish a menu"""
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from menus.models.menu import Menu

class PublishMenuView(TemplateView):
    """This view handles the request that publish
    a menu to Slack
    """

    def post(self, request, *args, **kwargs):
        """Publish a menu"""
        menu = Menu.objects.get(
            id=kwargs.get('id')
        )
        menu.publish()
        return HttpResponseRedirect('/menus/')
