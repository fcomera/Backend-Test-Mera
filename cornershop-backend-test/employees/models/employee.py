"""This module contains the specification of the model responsible
of managing the employees of the corporate."""
from django.db import models
from .managers.employee_manager import EmployeeeManager


class Employee(models.Model):
    """An employee is a person that works for cornershop
    and for now that has a Slack account. This model
    stores the information of the employees and the user
    associated to them. Also in order to keep the data
    connected to Slack it also stores the slack id of
    all the employees"""
    name = models.TextField(
        'The username in slack of the employee'
    )
    slack_user = models.TextField(
        'The slack user identifier in slack of the employee'
    )
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE
    )
    objects = EmployeeeManager()
