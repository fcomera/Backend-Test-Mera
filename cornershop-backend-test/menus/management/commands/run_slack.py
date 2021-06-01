"""This module contains the specification of the command able
to manage the incoming events and actions that come from Slack"""
from django.core.management.base import BaseCommand, CommandError

from slack_bolt import App

from backend_test.envtools import getenv

from employees.exceptions import OutOfTime

from menus.exceptions import NotSelectedOption, NotMenuAvailable, NotValidMenuOption
from menus.models.slack_model import SlackModel


app = App(
    token=getenv("SLACK_BOT_TOKEN"),
    signing_secret=getenv("SLACK_SIGNING_SECRET")
)

@app.action("gomenu")
def gomenu(ack, body, client):
    """This method is responsible of managing the action that
    is sent when the user press the Click Me button"""
    ack()
    user = body['user']
    try:
        SlackModel.create_order(body)
        client.chat_postMessage(
            text='Orden recibida',
            channel=body['channel']['id']
        )
    except NotSelectedOption:
        client.chat_postMessage(
            text='Selección inválida',
            channel=body['channel']['id']
        )
    except NotMenuAvailable:
        client.chat_postMessage(
            text='Menú del día inexistente',
            channel=body['channel']['id']
        )
    except NotValidMenuOption:
        client.chat_postMessage(
            text='La opción seleccionada no pertenece al menú del día',
            channel=body['channel']['id']
        )
    except OutOfTime:
        client.chat_postMessage(
            text='Ya acabó el tiempo para envíar o actualizar tu orden',
            channel=body['channel']['id']
        )

class Command(BaseCommand):
    """This command when executed runs the server that
    waits for user actions in the Slack workspace"""
    def handle(self, *args, **options):
        app.start(port=3000)
