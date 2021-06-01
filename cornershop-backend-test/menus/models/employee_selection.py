"""This module contains the specification of the model responsible
of managing the orders of the employees in corporate."""
from django.db import models

class EmployeeSelection(models.Model):
    """This model contains the reference of an option
    of a menu and the employee that is the propetary
    of that order. We require this menu in order to
    store also the customization of a selected option."""
    menu_option = models.ForeignKey(
        'MenuOption',
        on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE
    )
    customization = models.TextField(null=True)
