"""This view is responsible of showing the list of
orders or an specific employee. If the logged user
comes is the manager of the system it will automatically
redirect it to the view that obtain the menus of the day."""
from datetime import datetime

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden

from menus.models.employee_selection import EmployeeSelection


class EmployeeSelectionsList(TemplateView):
    """This view returns the orders of an specific user.
    Otherwise it will redirect to the view that shows
    the menus in the system"""
    template_name = 'list_orders.html'

    def get_context_data(self, **kwargs):
        """Sets the context for the template. If the
        authenticated user is a manager it will show
        a forbidden response."""
        if self.request.user and self.request.user.is_superuser:
            return HttpResponseForbidden()
        context = super().get_context_data(**kwargs)
        order_today = EmployeeSelection.objects.filter(
            menu_option__menu__date=datetime.now().date()
        ).first()
        orders = EmployeeSelection.objects.select_related('menu_option').filter(
            employee_id=self.request.user.employee.id
        ).exclude(id=order_today.id)
        context['orders'] = orders
        context['menu_today'] = order_today
        return context

    def get(self, request, *args, **kwargs):
        """Redirects when the user is superuser or
        shows the template when the user is not superuser"""
        if request.user and request.user.is_superuser:
            return HttpResponseRedirect('/menus/')
        return super().get(request, *args, **kwargs)
