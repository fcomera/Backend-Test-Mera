"""This module contains the specification of the Menu model an its
associated methods."""
from django.db import models
from django.conf import settings

import uuid

from backend_test.celery import app

from .menu_option import MenuOption
from .managers.menu_manager import MenuManager

from menus.exceptions import NotValidMenuOption

class Menu(models.Model):
    """Its the object capable of manage the options that can
    be served on an specific day for the employees."""
    id = models.UUIDField(
        'The identifier field of the menu',
        primary_key=True,
        default=uuid.uuid4
    )
    name = models.TextField(
        'The name of the menu that is going to be served.'
    )
    date = models.DateField(
        'The date which the menu is going to be served.'
    )
    expiration_date_time = models.DateTimeField(
        'The limited date and time to request an option of a menu'
    )
    is_published = models.BooleanField(
        default=False
    )
    objects = MenuManager()

    def publish(self):
        """This method is in charge of calling the
        task that will send a message to the users in a certain
        group with the options of the menu in an specific day"""
        app.send_task('menus.tasks.publish_menu', (self.id,))

    def get_options_for_slack(self):
        """Returns the list of elements that are
        part of a particular day in a format that
        can be interpreted by slack. The value of
        an option is always string because of the
        slack specification.

        :return: The list of menu options with elements
                 with the next format.
                 {
                    value: Uses the id of the option,
                    text: {
                        type: Always as plain_text,
                        text: A formatted text that contains the
                        concat of the option name and the option
                        description
                    }

                 }
        :rtype list
        """
        return [
            {
                'value': str(option.id),
                'text': {
                    'type': 'plain_text',
                    'text': '%s %s' % (
                        option.name,
                        option.description
                    )
                }
            }
            for option in self.menuoption_set.all().iterator()
        ]

    def get_option(self, option_id):
        """Returns an option of a menu based on the id.
        As slack manages id's in radio buttons as strings
        it is required to parse the option_id parameter
        into an integer.

        :param option_id: The id of selected option
        :type  option_id: str

        :return:    A reference to a valid option
                    of the current menu
        :rtype      MenuOption
        """
        option_id = int(option_id)
        option = self.menuoption_set.filter(
            id=option_id
        )
        if option.exists():
            return option.first()
        raise NotValidMenuOption

