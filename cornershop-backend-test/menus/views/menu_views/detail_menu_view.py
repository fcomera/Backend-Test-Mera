"""This module contains the specification of the view responsible
of showing the details of a menu"""
from django.views.generic import TemplateView

from menus.models.menu import Menu

class DetailMenuView(TemplateView):
    """This view renders the template required of showing
    the details of an specific menu
    """
    template_name = 'menu_detail.html'

    def get_context_data(self, **kwargs):
        """This method obtains the context data
        required to render to template"""
        context = super().get_context_data(**kwargs)
        context['menu'] = Menu.objects.get(
            id=kwargs.get('id')
        )
        return context
