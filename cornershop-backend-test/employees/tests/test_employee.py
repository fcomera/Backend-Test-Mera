"""This module contains the tests that verifies that
it is possible to create and update an order"""
from datetime import datetime
from datetime import timedelta

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from pytz import timezone

from employees.models.employee import Employee

from menus.models.menu import Menu


class EmployeesTestCase(TestCase):
    """This class executes the required test cases
    to validate the creation of orders and employees."""
    fixtures = ['Menus', 'MenusOption', 'Employee', 'EmployeeSelection']
    slack_employee = {
        'username': 'fcomera.ipn.mx',
        'slack_user_id': '1T123'
    }
    example_order = {
        'option': '1',
        'customization': 'Ex',
        'slack_user_id': '1T123',
        'username': 'abcde'
    }

    def _update_menu_date(self):
        """This method intends to update the date and the
        expiration date time of the pre registered menu"""
        tz = timezone(settings.TIME_ZONE)
        date = tz.localize(datetime.now())
        menu = Menu.objects.get(id=1)
        menu.date = date.date()
        menu.expiration_date_time = date + timedelta(hours=11)
        menu.save()

    def test_create_employee_from_slack(self):
        """This test verifies that the employee manager is
        capable of creating new users and new employees"""
        empleado = Employee.objects.create_employee(
            '1T1',
            'fcomera.ipn.mx'
        )
        queryset = Employee.objects.filter(
            slack_user='1T1'
        )
        self.assertTrue(queryset.count() == 1)
        queryset = User.objects.filter(
            username='fcomera.ipn.mx'
        )
        self.assertTrue(queryset.count() == 1)

    def test_create_order(self):
        """This method verifies that the employee manager creates a
        new order if it does not exists in the system"""
        self._update_menu_date()
        employee_selection = Employee.objects.create_update_order(
            **self.example_order
        )
        self.assertTrue(employee_selection)

    def test_update_order(self):
        """This method verifies that the employee manager updates a
        pre registered order."""
        self._update_menu_date()
        employee_selection = Employee.objects.create_update_order(
            **self.example_order
        )
        self.example_order.update(
            {
                'option': '2'
            }
        )
        self.assertTrue(
            employee_selection.menu_option_id == 1
        )
        employee_selection = Employee.objects.create_update_order(
                **self.example_order
        )
        self.assertTrue(employee_selection)
        self.assertTrue(
            employee_selection.menu_option_id == 2
        )
