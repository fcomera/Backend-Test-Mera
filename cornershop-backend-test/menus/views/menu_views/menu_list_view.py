"""This module contains the specification of the view that
shows the menus registered in the system"""
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied

from menus.models.menu import Menu
from menus.exceptions import NotMenuAvailable


class ListMenuView(TemplateView):
    """This view renders the template that
    shows the list of menus."""
    template_name = 'list_menus.html'

    def get_context_data(self, **kwargs):
        """Obtains the menus registered in the system"""
        if not self.request.user:
            raise PermissionDenied()
        if self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        try:
            context['menu'] = Menu.objects.get_menu_of_current_date()
            context['menus'] = Menu.objects.exclude(
                id=context['menu'].id
            )
        except NotMenuAvailable:
            context['menu'] = None
            context['menus'] = Menu.objects.all()
        return context
