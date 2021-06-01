"""This module contains the specification of the options
available on a menu."""

from django.db import models

class MenuOption(models.Model):
    """The objects of this class or this model contains the
    information related to the options that can be selected
    by an employee from an specific menu."""
    name = models.TextField(
        'The name of an option'
    )
    description = models.TextField(
        'The description of a menu. It can contains ingredients'
        ' or other required specification in order to let know '
        ' the employees the things used to prepare an option.'
    )
    menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
    )
    employees = models.ManyToManyField(
        'employees.Employee',
        through='EmployeeSelection'
    )
