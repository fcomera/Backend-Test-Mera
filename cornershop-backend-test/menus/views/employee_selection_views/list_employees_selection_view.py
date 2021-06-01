"""This module contains the specification of the view that
shows a list of the selected options by the employees"""
from django.core.exceptions import PermissionDenied

from menus.views.menu_views.detail_menu_view import DetailMenuView

from menus.models.menu import Menu


class ListEmployeesSelectionView(DetailMenuView):
    """View that renders the employees selection
    of a menu.
    """
    template_name = 'list_employees_selection.html'

    def get_context_data(self, **kwargs):
        """Obtains the menu in order to show its details"""
        if self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied()
        context = super().get_context_data(**kwargs)
        context['menu'] = Menu.objects.get(
            id=kwargs.get('id')
        )
        return context
