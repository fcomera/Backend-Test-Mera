"""This module contains the specification of the Manager
responsible of manupilating menu records.
"""
from datetime import datetime
from datetime import timedelta

from pytz import timezone

from django.db import models
from django.conf import settings

from menus.exceptions import NotMenuAvailable
from menus.models.menu_option import MenuOption

# The default hour of day for expiration
DEFAULT_HOUR_OF_DAY = 11

class MenuManager(models.Manager):
    """This manager inherits from models.Manager. This
    is because we require to implement new methods in
    order to create menus and its options."""

    def get_menu_of_current_date(self):
        """This method obtains the current date
        menu so a new order for that menu
        can be created"""
        tz = timezone(settings.TIME_ZONE)
        date = tz.localize(datetime.now()).date()
        menu_date = self.filter(
            date=date
        )
        if menu_date.exists():
            return menu_date.first()
        raise NotMenuAvailable()

    def create_menu(self, data):
        """This method creates a new menu record from
        a dictionary containing the corrspondant
        fields values. If the expiration date is not
        set by the user it means that the system requires
        to calculate it from the same date.

        :param data: Dictonary containing the data that
                     will be stored
        :type data: dictionary

        :return: The reference to the created menu
        :rtype:  Menu
        """
        tz = timezone(settings.TIME_ZONE)
        local_date = tz.localize(
            datetime.strptime(
                data.pop('date'),
                '%Y-%m-%d'
            )
        )
        data.update(
            {
                'date': local_date
            }
        )
        if 'expiration_date_time' in data:
            expiration_date_time = datetime.strptime(
                data.pop('expiration_date_time'),
                '%Y-%m-%d %H:%M:%S'
            )
            expiration_date_time = tz.localize(
                expiration_date_time
            )
            data.update(
                {
                    'expiration_date_time': expiration_date_time
                }
            )
        if 'expiration_date_time' not in data:
            expiration_date_time = local_date + timedelta(hours=DEFAULT_HOUR_OF_DAY)
            data.update(
                {
                    'expiration_date_time': expiration_date_time
                }
            )
        options = data.pop('options')
        instance = self.create(**data)
        empty = [
            opt.update(
                {
                    'menu': instance
                }
            )
            for opt in options
        ]
        bulk = [ MenuOption(**opt) for opt in options ]
        del empty
        MenuOption.objects.bulk_create(bulk)
        return instance
