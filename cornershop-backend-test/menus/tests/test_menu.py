"""This module contains the unit tests responsible of
validating the code in the menu application"""
from datetime import datetime

from pytz import timezone

from django.test import TestCase
from django.conf import settings

from menus.models.menu import Menu
from menus.models.menu_option import MenuOption
from menus.forms.menu_forms.create_menu_form import CreateMenuForm
from menus.tasks import publish_menu

class MenusTestCase(TestCase):
    """This class verifies that a menu can be created
    and that the options of a menu can be obtained
    """
    fixtures = ['Menus', 'MenusOption']
    test_data = {
        'name': 'Menu 1',
        'date': '2021-01-01',
        'expiration_date_time': '2021-01-02 11:00:00',
        'options': [
            {
                'name': 'Option 1',
                'description': 'Description 1'
            }
        ]
    }
    test_data_two = {
        'name': 'Menu 1',
        'date': '2021-01-01',
        'options': [
            {
                'name': 'Option 1',
                'description': 'Description 1'
            }
        ]
    }

    def test_create_menu_with_expiration(self):
        """This method verifes that the Menu manager creates
        a menu when the expiration_date_time field is in the
        data."""
        menu = Menu.objects.create_menu(self.test_data)
        self.assertTrue(menu)
        self.assertTrue(menu.id)
        self.assertTrue(menu.menuoption_set.all().count(), 1)

    def test_create_menu(self):
        """This method verifies that the Menu manager creates
        a menu when the expiration_date_time field is not
        in the data"""
        tz = timezone(settings.TIME_ZONE)
        menu = Menu.objects.create_menu(self.test_data_two)
        self.assertTrue(menu)
        self.assertTrue(menu.id)
        self.assertTrue(menu.expiration_date_time == tz.localize(datetime(2021, 1, 1, 11, 0)))
        self.assertTrue(menu.menuoption_set.all().count(), 1)

    def test_get_menu_options_for_slack(self):
        """This test verifies that the get_options_for_slack
        method of the Menu model returs a valid dictionary
        that Slack can handle"""
        menu = Menu.objects.get(id=1)
        data = menu.get_options_for_slack()
        self.assertTrue(
            [
                {
                    'value': '1',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Option 1 Description'
                    }
                },
                {
                    'value': '2',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Option 2 Description 2'
                    }
                }
            ] == data
        )

    def test_publish_menu_task(self):
        """This test verifies that a menu is published,
        meaning it will be sent to the users added in
        the food group in Slack."""
        task = publish_menu.apply(
            args=(1, ),
        ).get()
        menu = Menu.objects.get(id=1)
        self.assertTrue(menu.is_published)
