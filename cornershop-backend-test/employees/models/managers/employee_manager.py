"""This module contains the specification of the manager responsible
of employee model records."""
from datetime import datetime

from pytz import timezone

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from menus.models.menu import Menu
from menus.models.employee_selection import EmployeeSelection

from employees.exceptions import OutOfTime

class EmployeeeManager(models.Manager):
    """This manager is responsible of manipulate or take care
    about the employee records."""

    def create_employee(self, slack_user_id, username):
        """This method creates a new user and a new employee
        if it does not exists in the application.

        :param slack_user_id: A string containing the slack identifier
                              of the employee.
        :type slack_user_id: str
        :param username: A string containing the username that
                         will be used to create a new user for
                         a non registered employee
        :type username: str

        :return: Returns the reference of the new created employee
        :rtype:  Employee
        """
        user = User.objects.create_user(
            username,
            password='test123'
        )
        user.save()
        employee = self.create(
            **{
                'user': user,
                'name': username,
                'slack_user': slack_user_id
            }
        )
        return employee

    def create_update_order(self, **data):
        """This method creates or updates an order(or selection)
        of an employee. The process is this:

        - The method obtains the menu published for the
          current date. If there is no menu a NotMenuAvailable
          exception will be thrown.
        - The method obtains the selected option incoming in the
          data dictionary. The option must be a child or a related
          object of the menu obtained in the previous step so a new
          selection can be created.
        - The method search for an employee by his/her slack user
        identifier. If the employee exists it obtains that reference.
        In the other case it creates a new employee.
        - The method search for a previous selection or order. If
        an order for the menu exists it returns that reference
        and updates its values with the incoming data. If a
        selection does not exists then it will create a new one.

        :param data: Dictionary containing the values for a new
                     or a previous registered order
        :type  data: dict

        :return: Reference to the new employee selection or the
                 previous registered one.
        :rtype:  EmployeeSelection
        """
        tz = timezone(settings.TIME_ZONE)
        date = tz.localize(datetime.now())
        menu = Menu.objects.get_menu_of_current_date()
        if tz.localize(menu.expiration_date_time) < date:
            raise OutOfTime
        option = menu.get_option(data.get('option'))
        employee = None
        employee_qs = self.filter(
            slack_user=data.get('slack_user_id')
        )
        if not employee_qs.exists():
            employee = self.create_employee(
                data.get('slack_user_id'),
                data.get('username')
            )
        if employee_qs.exists():
            employee =  employee_qs.first()
        employee_selection = EmployeeSelection.objects.filter(
            employee_id=employee.id,
            menu_option__menu_id=menu.id
        )
        if not employee_selection.exists():
            employee_selection = EmployeeSelection.objects.create(
                **{
                    'menu_option': option,
                    'employee': employee,
                    'customization': data.get('customization', None)
                }
            )
            return employee_selection
        employee_selection =  employee_selection.first()
        employee_selection.menu_option = option
        employee_selection.customization = data.get('customization', None)
        employee_selection.save()
        return employee_selection
